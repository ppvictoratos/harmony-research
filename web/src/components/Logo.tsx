/** Brand mark: brain outline with treble and bass clefs. Colors follow the app theme (see .logo in App.css). */
export function Logo({ size = 56 }: { size?: number }) {
  return (
    <svg className="logo" viewBox="0 0 120 100" width={size} height={(size * 100) / 120} aria-hidden="true">
      <path
        className="logo-brain"
        d="M55 72 C 41 73 31 70 26 64 C 18 62 14 54 17 47 C 12 41 14 31 22 28 C 22 19 30 13 39 15 C 44 8 55 7 62 11 C 70 6 82 8 87 16 C 96 16 103 24 101 33 C 107 39 106 50 99 54 C 98 63 89 68 80 66 C 76 71 71 73 65 72"
      />
      <path className="logo-fold" d="M24 42 C 29 37 36 38 39 43" />
      <path className="logo-fold" d="M27 56 C 32 52 38 53 41 57" />
      <path className="logo-fold" d="M73 19 C 79 16 86 19 89 24" />
      <path
        className="logo-clef"
        d="M60 86 C 56 89 51 87 51 82 C 51 78 56 77 58 80 C 60 84 63 80 62 74 L 56 24 C 55 15 61 10 65 15 C 69 21 62 30 54 38 C 46 46 43 55 49 61 C 55 67 67 65 69 56 C 71 47 62 42 56 46 C 51 50 53 57 58 57"
      />
      <circle className="logo-dot" cx="76" cy="37" r="2.6" />
      <path className="logo-bass" d="M76 37 C 76 30 87 29 87 38 C 87 47 81 53 74 57" />
      <circle className="logo-dot" cx="92" cy="35" r="2.2" />
      <circle className="logo-dot" cx="92" cy="43" r="2.2" />
      <path className="logo-swoosh" d="M6 84 Q 60 74 114 84 Q 60 79 6 84 Z" />
    </svg>
  );
}
