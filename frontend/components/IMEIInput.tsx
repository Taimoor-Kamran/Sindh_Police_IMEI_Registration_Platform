"use client";

import { useState } from "react";

interface IMEIInputProps {
  value: string;
  onChange: (value: string) => void;
}

function luhnCheck(imei: string): boolean {
  if (imei.length !== 15 || !/^\d{15}$/.test(imei)) return false;
  let total = 0;
  for (let i = 0; i < imei.length; i++) {
    let n = parseInt(imei[i]);
    if (i % 2 === 1) {
      n *= 2;
      if (n > 9) n -= 9;
    }
    total += n;
  }
  return total % 10 === 0;
}

export default function IMEIInput({ value, onChange }: IMEIInputProps) {
  const [touched, setTouched] = useState(false);

  const isValid = value.length === 0 || luhnCheck(value);
  const showError = touched && value.length > 0 && !luhnCheck(value);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        IMEI Number
      </label>
      <input
        type="text"
        maxLength={15}
        value={value}
        onChange={(e) => {
          const val = e.target.value.replace(/\D/g, "");
          onChange(val);
        }}
        onBlur={() => setTouched(true)}
        placeholder="Enter 15-digit IMEI"
        className={`w-full px-4 py-3 rounded-lg border ${
          showError
            ? "border-red-400 focus:ring-red-300 focus:border-red-400"
            : "border-gray-300 focus:ring-primary/30 focus:border-primary"
        } focus:outline-none focus:ring-2 transition-colors font-mono tracking-wider`}
      />
      <div className="flex items-center justify-between mt-1">
        <p className={`text-xs ${showError ? "text-red-500" : "text-gray-400"}`}>
          {showError
            ? "Invalid IMEI. Must be 15 digits with valid Luhn checksum"
            : `${value.length}/15 digits`}
        </p>
        {value.length === 15 && isValid && (
          <span className="text-xs text-green-600 font-medium">Valid IMEI</span>
        )}
      </div>
    </div>
  );
}

export { luhnCheck };
