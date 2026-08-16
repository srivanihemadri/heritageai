export default function HeroBackground() {
  return (
    <div
      className="pointer-events-none absolute inset-0 -z-10 overflow-hidden"
      aria-hidden="true"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(212,175,90,0.11),transparent_38%)]" />

      <div className="absolute left-[-18rem] top-[-14rem] h-[38rem] w-[38rem] rounded-full bg-[rgba(212,175,90,0.055)] blur-[120px]" />

      <div className="absolute right-[-16rem] top-[18%] h-[34rem] w-[34rem] rounded-full bg-[rgba(155,117,48,0.045)] blur-[120px]" />

      <div className="absolute inset-x-0 bottom-0 h-64 bg-gradient-to-t from-[var(--heritage-black)] to-transparent" />

      <div className="absolute inset-0 opacity-[0.025] [background-image:linear-gradient(rgba(247,241,230,0.7)_1px,transparent_1px),linear-gradient(90deg,rgba(247,241,230,0.7)_1px,transparent_1px)] [background-size:72px_72px]" />
    </div>
  );
}
