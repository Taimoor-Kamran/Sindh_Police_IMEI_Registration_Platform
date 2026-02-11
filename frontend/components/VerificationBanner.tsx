"use client";

import { AlertTriangle } from "lucide-react";

export default function VerificationBanner() {
  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6 flex items-start gap-3">
      <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
      <div>
        <h3 className="text-sm font-semibold text-yellow-800">
          Verification Pending
        </h3>
        <p className="text-sm text-yellow-700 mt-1">
          Your shop keeper account is pending verification by police admin. You
          will be able to register devices for customers once verified.
        </p>
      </div>
    </div>
  );
}
