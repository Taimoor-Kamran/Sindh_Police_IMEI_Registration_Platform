"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { Smartphone, Loader2, CheckCircle } from "lucide-react";
import IMEIInput, { luhnCheck } from "@/components/IMEIInput";
import { mobileApi } from "@/lib/api";

export default function RegisterDevicePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [form, setForm] = useState({
    imei: "",
    mobile_number: "",
    brand: "",
    model: "",
    notes: "",
  });

  const updateField = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (!luhnCheck(form.imei)) {
      setError("Please enter a valid 15-digit IMEI number");
      return;
    }

    if (!form.mobile_number) {
      setError("Mobile number is required");
      return;
    }

    setLoading(true);
    try {
      await mobileApi.registerSelf({
        imei: form.imei,
        mobile_number: form.mobile_number,
        brand: form.brand || undefined,
        model: form.model || undefined,
        notes: form.notes || undefined,
      });
      setSuccess(true);
      setTimeout(() => router.push("/dashboard"), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
        <h2 className="text-xl font-bold text-gray-800">Device Registered!</h2>
        <p className="text-gray-500 mt-2">Redirecting to dashboard...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Register Your Device</h1>
        <p className="text-gray-500 mt-1">
          Register your mobile device with the IMEI number for protection
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 max-w-xl">
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <IMEIInput
            value={form.imei}
            onChange={(v) => updateField("imei", v)}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Device Mobile Number
            </label>
            <input
              type="text"
              value={form.mobile_number}
              onChange={(e) => updateField("mobile_number", e.target.value)}
              placeholder="03XX-XXXXXXX"
              required
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Brand
              </label>
              <input
                type="text"
                value={form.brand}
                onChange={(e) => updateField("brand", e.target.value)}
                placeholder="e.g. Samsung"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Model
              </label>
              <input
                type="text"
                value={form.model}
                onChange={(e) => updateField("model", e.target.value)}
                placeholder="e.g. Galaxy S24"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes (optional)
            </label>
            <textarea
              value={form.notes}
              onChange={(e) => updateField("notes", e.target.value)}
              placeholder="Any additional details..."
              rows={3}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors resize-none"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white font-semibold py-3 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Registering...
              </>
            ) : (
              <>
                <Smartphone className="w-5 h-5" />
                Register Device
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
