from app.services.ai.image.contract import ImageEnhancementResponse
from app.services.ai.image.service import ImageEnhancementService
from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.api.v1.contracts.ai import (
    GroundedAnswerErrorResponse,
    GroundedAnswerRequest,
    GroundedAnswerResponse,
    GroundedAnswerSourceResponse,
    VoiceGuideResponse,
)
from app.db.session import get_db
from app.services.ai.generation import (
    GeminiQuotaExceededError,
    GeminiProviderError,
    GeminiProviderTimeoutError,
    GroundedAnswerService,
)
from app.repositories.scan import ScanRepository
from app.services.ai.scanner.service import (
    HeritageScannerService,
    ScannerQuotaExceededError,
)
from app.services.ai.scanner.image import ScannerImageValidationError
from app.services.ai.voice import (
    VoiceResponse,
    VoiceService,
)
from app.services.ai.voice.audio import (
    VoiceAudioValidationError,
)
from app.services.ai.voice_guide import (
    VoiceGuideService,
)
from app.services.storage import media_storage

from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/answer",
    response_model=GroundedAnswerResponse,
    responses={
        422: {
            "model": GroundedAnswerErrorResponse,
            "description": "Invalid request.",
        },
        429: {
            "model": GroundedAnswerErrorResponse,
            "description": "Gemini generation quota exceeded.",
        },
        502: {
            "model": GroundedAnswerErrorResponse,
            "description": "Gemini provider error.",
        },
        504: {
            "model": GroundedAnswerErrorResponse,
            "description": "Gemini provider timeout.",
        },
        500: {
            "model": GroundedAnswerErrorResponse,
            "description": "AI answer generation failure.",
        },
    },
)
def grounded_answer(
    request: GroundedAnswerRequest,
) -> GroundedAnswerResponse:

    service = None

    try:
        service = GroundedAnswerService()

        result = service.answer(
            query=request.question,
            top_k=request.top_k,
        )

        return GroundedAnswerResponse(
            query=result.query,
            answer=result.answer,
            sources=[
                GroundedAnswerSourceResponse(
                    rank=source.rank,
                    chunk_id=source.chunk_id,
                    document_id=source.document_id,
                    title=source.title,
                    similarity_score=source.similarity_score,
                    provenance_level=source.provenance_level,
                    is_verified=source.is_verified,
                )
                for source in result.sources
            ],
            grounded=result.grounded,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except GeminiQuotaExceededError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "GEMINI_QUOTA_EXCEEDED",
                "message": str(exc),
            },
        ) from exc

    except GeminiProviderTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "code": "GEMINI_PROVIDER_TIMEOUT",
                "message": str(exc),
            },
        ) from exc

    except GeminiProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": "GEMINI_PROVIDER_ERROR",
                "message": str(exc),
            },
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Grounded answer generation failed.",
        ) from exc

    finally:
        if service is not None:
            service.close()

@router.post(
    "/scan",
    response_model=HeritageScannerResponse,
    responses={
        400: {
            "description": "Invalid image",
        },
        401: {
            "description": "Authentication required",
        },
        429: {
            "description": "Scanner quota exceeded",
        },
        413: {
            "description": "Image too large",
        },
        422: {
            "description": "Invalid upload",
        },
        500: {
            "description": "Scanner failure",
        },
    },
)
async def heritage_scan(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> HeritageScannerResponse:
    """Analyze an uploaded heritage image with multimodal AI."""

    service = None

    try:
        if not file.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "INVALID_IMAGE",
                    "message": "Image content type is required.",
                },
            )

        if file.content_type.lower() not in {
            "image/jpeg",
            "image/png",
            "image/webp",
        }:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "UNSUPPORTED_IMAGE",
                    "message": "Only JPEG, PNG, and WEBP images are supported.",
                },
            )

        image_bytes = await file.read()

        service = HeritageScannerService()

        result = service.scan(
            image_bytes=image_bytes,
            content_type=file.content_type.lower(),
        )

        repository = ScanRepository(db)

        scan = repository.create(
            result=result.result,
        )

        db.commit()
        db.refresh(scan)

        return HeritageScannerResponse(
            success=True,
            scan_id=str(scan.id),
            result=result.result,
        )

    except ScannerImageValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_IMAGE",
                "message": str(exc),
            },
        ) from exc

    except ScannerQuotaExceededError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "SCANNER_QUOTA_EXCEEDED",
                "message": str(exc),
            },
        ) from exc

    except HTTPException:
        raise

    except Exception as exc:
        print(
            "Heritage scanner request failed:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SCANNER_FAILURE",
                "message": "Heritage image scanning failed.",
            },
        ) from exc

    finally:
        if service is not None:
            client = getattr(service, "client", None)

            close_method = getattr(
                client,
                "close",
                None,
            )

            if callable(close_method):
                try:
                    close_method()
                except Exception:
                    pass



@router.get(
    "/scans/{scan_id}",
    response_model=HeritageScannerResponse,
)
def get_scan(
    scan_id: str,
    db: Session = Depends(get_db),
) -> HeritageScannerResponse:

    repository = ScanRepository(db)

    scan = repository.get_by_id(
        scan_id=scan_id,
    )

    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "SCAN_NOT_FOUND",
                "message": "Scan not found.",
            },
        )

    result = HeritageScannerResult(
        identified_name=scan.identified_name,
        identification_status=scan.identification_status,
        evidence_quality=scan.evidence_quality,
        category=scan.category,
        location=scan.location,
        country=scan.country,
        confidence=scan.confidence,
        confidence_level=scan.confidence_level,
        description=scan.description,
        architectural_style=scan.architectural_style,
        historical_period=scan.historical_period,
        historical_significance=scan.historical_significance,
        visual_evidence=scan.visual_evidence,
        alternative_matches=scan.alternative_matches,
        grounding_status=scan.grounding_status,
    )

    return HeritageScannerResponse(
        success=True,
        scan_id=str(scan.id),
        result=result,
    )


@router.get(
    "/scans",
    response_model=list[HeritageScannerResponse],
)
def list_scans(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> list[HeritageScannerResponse]:

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="limit must be between 1 and 100.",
        )

    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="offset must be >= 0.",
        )

    repository = ScanRepository(db)

    scans = repository.list_all(
        limit=limit,
        offset=offset,
    )

    responses = []

    for scan in scans:
        result = HeritageScannerResult(
            identified_name=scan.identified_name,
            identification_status=scan.identification_status,
            evidence_quality=scan.evidence_quality,
            category=scan.category,
            location=scan.location,
            country=scan.country,
            confidence=scan.confidence,
            confidence_level=scan.confidence_level,
            description=scan.description,
            architectural_style=scan.architectural_style,
            historical_period=scan.historical_period,
            historical_significance=scan.historical_significance,
            visual_evidence=scan.visual_evidence,
            alternative_matches=scan.alternative_matches,
            grounding_status=scan.grounding_status,
        )

        responses.append(
            HeritageScannerResponse(
                success=True,
                scan_id=str(scan.id),
                result=result,
            )
        )

    return responses

@router.post(
    "/voice",
    response_model=VoiceResponse,
    responses={
        400: {
            "description": "Invalid audio",
        },
        401: {
            "description": "Authentication required",
        },
        413: {
            "description": "Audio too large",
        },
        422: {
            "description": "Unsupported audio",
        },
        500: {
            "description": "Voice transcription failure",
        },
    },
)
async def ai_voice(
    file: UploadFile = File(...),
) -> VoiceResponse:
    """Transcribe authenticated user voice input."""

    service = None

    try:
        if not file.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "INVALID_AUDIO",
                    "message": "Audio content type is required.",
                },
            )

        audio_bytes = await file.read()

        service = VoiceService()

        result = service.transcribe(
            audio_bytes=audio_bytes,
            content_type=file.content_type.lower(),
        )

        return VoiceResponse(
            success=True,
            result=result,
        )

    except VoiceAudioValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_AUDIO",
                "message": str(exc),
            },
        ) from exc

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "VOICE_TRANSCRIPTION_INVALID",
                "message": str(exc),
            },
        ) from exc

    except Exception as exc:
        print(
            "AI voice request failed:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "VOICE_TRANSCRIPTION_FAILED",
                "message": "Voice transcription failed.",
            },
        ) from exc

    finally:
        if service is not None:
            service.close()



@router.post(
    "/voice-guide",
    response_model=VoiceGuideResponse,
    responses={
        400: {
            "description": "Invalid audio",
        },
        401: {
            "description": "Authentication required",
        },
        422: {
            "description": "Invalid voice guide request",
        },
        500: {
            "description": "Voice guide failure",
        },
    },
)
async def ai_voice_guide(
    file: UploadFile = File(...),
) -> VoiceGuideResponse:
    """Run the complete authenticated HeritageAI Voice Guide pipeline."""

    import io
    import uuid
    import wave

    service = None

    try:
        if not file.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "INVALID_AUDIO",
                    "message": "Audio content type is required.",
                },
            )

        audio_bytes = await file.read()

        service = VoiceGuideService()

        result = service.process(
            audio_bytes=audio_bytes,
            content_type=file.content_type.lower(),
        )

        audio_url = None
        audio_mime_type = None
        audio_sample_rate = None

        if (
            result.tts_available
            and result.audio_bytes is not None
            and result.audio_sample_rate is not None
        ):
            wav_buffer = io.BytesIO()

            with wave.open(wav_buffer, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(result.audio_sample_rate)
                wav_file.writeframes(result.audio_bytes)

            wav_bytes = wav_buffer.getvalue()

            storage_key = (
                "voice-guide/"
                "anonymous/"
                f"{uuid.uuid4().hex}.wav"
            )

            audio_url = media_storage.save(
                content=wav_bytes,
                storage_key=storage_key,
            )

            audio_mime_type = "audio/wav"
            audio_sample_rate = result.audio_sample_rate

        return VoiceGuideResponse(
            success=True,
            transcript=result.transcript,
            language=result.language,
            confidence=result.confidence,
            answer=result.answer,
            grounded=result.grounded,
            sources=[
                GroundedAnswerSourceResponse(
                    rank=source.rank,
                    chunk_id=source.chunk_id,
                    document_id=source.document_id,
                    title=source.title,
                    similarity_score=source.similarity_score,
                    provenance_level=source.provenance_level,
                    is_verified=source.is_verified,
                )
                for source in result.sources
            ],
            audio_url=audio_url,
            audio_mime_type=audio_mime_type,
            audio_sample_rate=audio_sample_rate,
            tts_available=result.tts_available,
            tts_fallback_reason=result.tts_fallback_reason,
        )

    except VoiceAudioValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_AUDIO",
                "message": str(exc),
            },
        ) from exc

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "VOICE_GUIDE_INVALID",
                "message": str(exc),
            },
        ) from exc

    except Exception as exc:
        print(
            "AI voice guide request failed:",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "VOICE_GUIDE_FAILED",
                "message": "Voice Guide processing failed.",
            },
        ) from exc

    finally:
        if service is not None:
            service.close()


@router.post(
    "/image/enhance",
    response_model=ImageEnhancementResponse,
)
async def enhance_heritage_image(
    file: UploadFile = File(...),
    resolution: str = "2K",
):
    """Enhance a heritage image using Gemini image generation."""

    from fastapi.responses import Response

    try:
        image_bytes = await file.read()

        service = ImageEnhancementService()

        try:
            result = service.enhance(
                image_bytes=image_bytes,
                content_type=file.content_type or "",
                resolution=resolution,
            )
        finally:
            service.close()

        return Response(
            content=result.image_bytes,
            media_type=result.mime_type,
            headers={
                "X-HeritageAI-Resolution": result.resolution,
                "X-HeritageAI-Width": str(result.width),
                "X-HeritageAI-Height": str(result.height),
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "IMAGE_ENHANCEMENT_FAILED",
                "message": "Heritage image enhancement failed.",
            },
        ) from exc
