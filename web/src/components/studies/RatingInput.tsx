interface RatingInputProps {
  label: string;
  value: number | null;
  onChange: (value: number | null) => void;
}

/** 1-10 rating as a row of toggle buttons. Clicking the selected value clears it. */
export function RatingInput({ label, value, onChange }: RatingInputProps) {
  return (
    <fieldset className="rating">
      <legend>{label}</legend>
      <div className="rating-scale">
        {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
          <button
            key={n}
            type="button"
            aria-pressed={value === n}
            aria-label={`${label}: ${n}`}
            onClick={() => onChange(value === n ? null : n)}
          >
            {n}
          </button>
        ))}
      </div>
      <div className="rating-ends" aria-hidden="true">
        <span>low</span>
        <span>high</span>
      </div>
    </fieldset>
  );
}
