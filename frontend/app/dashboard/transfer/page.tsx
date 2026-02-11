"use client";

import { useState, useEffect, FormEvent } from "react";
import {
  Search,
  ArrowRightLeft,
  Loader2,
  CheckCircle,
  AlertTriangle,
  ShieldAlert,
  KeyRound,
} from "lucide-react";
import TransferHistory from "@/components/TransferHistory";
import {
  transferApi,
  deviceCheckApi,
  transferOtpApi,
  TransferRecord,
  DeviceCheckResult,
} from "@/lib/api";
import { getUserRole, isShopVerified } from "@/lib/auth";

const TRANSFER_TYPES = ["SALE", "GIFT", "INHERITANCE", "OTHER"];

function validateLuhn(imei: string): boolean {
  if (!/^\d{15}$/.test(imei)) return false;
  let total = 0;
  for (let i = 0; i < imei.length; i++) {
    let n = parseInt(imei[i], 10);
    if (i % 2 === 1) {
      n *= 2;
      if (n > 9) n -= 9;
    }
    total += n;
  }
  return total % 10 === 0;
}

// ─── Shopkeeper OTP Transfer Wizard ───

function ShopOTPTransfer() {
  const [step, setStep] = useState(1);
  const [imei, setImei] = useState("");
  const [oldOwnerIdentifier, setOldOwnerIdentifier] = useState("");
  const [newOwnerIdentifier, setNewOwnerIdentifier] = useState("");
  const [otpCode, setOtpCode] = useState("");
  const [transferType, setTransferType] = useState("SALE");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // Info from server
  const [oldOwnerName, setOldOwnerName] = useState("");
  const [deviceBrand, setDeviceBrand] = useState("");
  const [deviceModel, setDeviceModel] = useState("");
  const [newOwnerName, setNewOwnerName] = useState("");

  const reset = () => {
    setStep(1);
    setImei("");
    setOldOwnerIdentifier("");
    setNewOwnerIdentifier("");
    setOtpCode("");
    setTransferType("SALE");
    setNotes("");
    setError("");
    setSuccess(false);
    setOldOwnerName("");
    setDeviceBrand("");
    setDeviceModel("");
    setNewOwnerName("");
  };

  const handleStep1 = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (!imei.trim() || !validateLuhn(imei.trim())) {
      setError("Invalid IMEI. Must be 15 digits and pass Luhn check.");
      return;
    }
    if (!oldOwnerIdentifier.trim()) {
      setError("Please enter old owner's CNIC or phone number");
      return;
    }
    setLoading(true);
    try {
      const res = await transferOtpApi.initiate({
        imei: imei.trim(),
        old_owner_identifier: oldOwnerIdentifier.trim(),
      });
      setOldOwnerName(res.data.old_owner_name);
      setDeviceBrand(res.data.device_brand || "");
      setDeviceModel(res.data.device_model || "");
      setOtpCode("");
      setStep(2);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to initiate transfer");
    } finally {
      setLoading(false);
    }
  };

  const handleStep2 = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (!otpCode.trim() || otpCode.length !== 6) {
      setError("Please enter the 6-digit OTP code");
      return;
    }
    setLoading(true);
    try {
      await transferOtpApi.verifyOldOwner({
        imei: imei.trim(),
        old_owner_identifier: oldOwnerIdentifier.trim(),
        otp_code: otpCode.trim(),
      });
      setOtpCode("");
      setStep(3);
    } catch (err: any) {
      setError(err.response?.data?.detail || "OTP verification failed");
    } finally {
      setLoading(false);
    }
  };

  const handleStep3 = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (!newOwnerIdentifier.trim()) {
      setError("Please enter new owner's CNIC or phone number");
      return;
    }
    setLoading(true);
    try {
      const res = await transferOtpApi.sendNewOwnerOTP({
        imei: imei.trim(),
        new_owner_identifier: newOwnerIdentifier.trim(),
      });
      setNewOwnerName(res.data.new_owner_name);
      setOtpCode("");
      setStep(4);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to send OTP to new owner");
    } finally {
      setLoading(false);
    }
  };

  const handleStep4 = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (!otpCode.trim() || otpCode.length !== 6) {
      setError("Please enter the 6-digit OTP code");
      return;
    }
    setLoading(true);
    try {
      await transferOtpApi.complete({
        imei: imei.trim(),
        new_owner_identifier: newOwnerIdentifier.trim(),
        otp_code: otpCode.trim(),
        transfer_type: transferType,
        notes: notes || undefined,
      });
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Transfer failed");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
        <div className="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle className="w-8 h-8 text-green-600" />
        </div>
        <h3 className="text-lg font-semibold text-gray-800 mb-2">
          Transfer Completed Successfully!
        </h3>
        <p className="text-sm text-gray-500 mb-1">
          Device <span className="font-mono">{imei}</span> has been transferred.
        </p>
        <p className="text-sm text-gray-500 mb-6">
          {deviceBrand} {deviceModel} — from {oldOwnerName} to {newOwnerName}
        </p>
        <button
          onClick={reset}
          className="bg-primary text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-primary-light transition-colors"
        >
          New Transfer
        </button>
      </div>
    );
  }

  const steps = [
    { num: 1, label: "Identify Device" },
    { num: 2, label: "Verify Old Owner" },
    { num: 3, label: "New Owner" },
    { num: 4, label: "Complete" },
  ];

  return (
    <div>
      {/* Progress indicator */}
      <div className="flex items-center justify-between mb-8 max-w-2xl">
        {steps.map((s, i) => (
          <div key={s.num} className="flex items-center">
            <div className="flex flex-col items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                  step > s.num
                    ? "bg-green-500 text-white"
                    : step === s.num
                    ? "bg-primary text-white"
                    : "bg-gray-200 text-gray-500"
                }`}
              >
                {step > s.num ? "✓" : s.num}
              </div>
              <span className="text-xs mt-1 text-gray-500">{s.label}</span>
            </div>
            {i < steps.length - 1 && (
              <div
                className={`w-16 sm:w-24 h-0.5 mx-2 mb-5 ${
                  step > s.num ? "bg-green-500" : "bg-gray-200"
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        {step === 1 && (
          <form onSubmit={handleStep1} className="space-y-4 max-w-lg">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              <Search className="w-5 h-5 text-primary" />
              Step 1: Identify Device & Old Owner
            </h3>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Device IMEI
              </label>
              <input
                type="text"
                value={imei}
                onChange={(e) => setImei(e.target.value.replace(/\D/g, "").slice(0, 15))}
                placeholder="Enter 15-digit IMEI"
                maxLength={15}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Old Owner CNIC or Phone
              </label>
              <input
                type="text"
                value={oldOwnerIdentifier}
                onChange={(e) => setOldOwnerIdentifier(e.target.value)}
                placeholder="e.g. 12345-6789012-3 or 03001234567"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-primary text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <KeyRound className="w-4 h-4" />}
              Send OTP to Old Owner
            </button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleStep2} className="space-y-4 max-w-lg">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              <KeyRound className="w-5 h-5 text-primary" />
              Step 2: Verify Old Owner OTP
            </h3>
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-700">
              OTP sent to <strong>{oldOwnerName}</strong>. Ask the old owner for the 6-digit code.
            </div>
            <div className="text-sm text-gray-500">
              Device: {deviceBrand} {deviceModel} (IMEI: <span className="font-mono">{imei}</span>)
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                OTP Code
              </label>
              <input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                placeholder="Enter 6-digit OTP"
                maxLength={6}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors text-center text-2xl tracking-widest font-mono"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-primary text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle className="w-4 h-4" />}
              Verify OTP
            </button>
          </form>
        )}

        {step === 3 && (
          <form onSubmit={handleStep3} className="space-y-4 max-w-lg">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              <ArrowRightLeft className="w-5 h-5 text-primary" />
              Step 3: Identify New Owner
            </h3>
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700">
              Old owner <strong>{oldOwnerName}</strong> verified successfully.
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                New Owner CNIC or Phone
              </label>
              <input
                type="text"
                value={newOwnerIdentifier}
                onChange={(e) => setNewOwnerIdentifier(e.target.value)}
                placeholder="e.g. 55555-6666666-7 or 03201234567"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-primary text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <KeyRound className="w-4 h-4" />}
              Send OTP to New Owner
            </button>
          </form>
        )}

        {step === 4 && (
          <form onSubmit={handleStep4} className="space-y-4 max-w-lg">
            <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-primary" />
              Step 4: Complete Transfer
            </h3>
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-700">
              OTP sent to <strong>{newOwnerName}</strong>. Ask the new owner for the 6-digit code.
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                New Owner OTP Code
              </label>
              <input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                placeholder="Enter 6-digit OTP"
                maxLength={6}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors text-center text-2xl tracking-widest font-mono"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Transfer Type
              </label>
              <select
                value={transferType}
                onChange={(e) => setTransferType(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors bg-white"
              >
                {TRANSFER_TYPES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Notes (optional)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Transfer details..."
                rows={2}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors resize-none"
              />
            </div>
            <div className="flex items-center gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-yellow-600 shrink-0" />
              <p className="text-xs text-yellow-700">
                By proceeding, you confirm this is a legal ownership transfer.
              </p>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-primary text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <ArrowRightLeft className="w-4 h-4" />}
              Complete Transfer
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

// ─── Citizen Check & Transfer (existing flow) ───

function CitizenTransfer() {
  const [transfers, setTransfers] = useState<TransferRecord[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(true);

  const [imei, setImei] = useState("");
  const [checking, setChecking] = useState(false);
  const [checkResult, setCheckResult] = useState<DeviceCheckResult | null>(null);
  const [checkError, setCheckError] = useState("");

  const [transferType, setTransferType] = useState("SALE");
  const [notes, setNotes] = useState("");
  const [transferring, setTransferring] = useState(false);
  const [transferError, setTransferError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    transferApi.list().then((res) => setTransfers(res.data)).catch(() => {}).finally(() => setLoadingHistory(false));
  }, []);

  const handleCheck = async (e: FormEvent) => {
    e.preventDefault();
    setCheckError("");
    setCheckResult(null);
    setSuccess(false);
    if (!imei.trim()) { setCheckError("Please enter an IMEI number"); return; }
    if (!validateLuhn(imei.trim())) { setCheckError("Invalid IMEI. Must be 15 digits and pass Luhn check."); return; }
    setChecking(true);
    try {
      const res = await deviceCheckApi.check(imei.trim());
      setCheckResult(res.data);
    } catch (err: any) {
      setCheckError(err.response?.data?.detail || "Failed to check device");
    } finally {
      setChecking(false);
    }
  };

  const handleTransfer = async (e: FormEvent) => {
    e.preventDefault();
    setTransferError("");
    setTransferring(true);
    try {
      await deviceCheckApi.transfer({ imei: imei.trim(), transfer_type: transferType, notes: notes || undefined });
      setSuccess(true);
      setCheckResult(null);
      setImei("");
      setNotes("");
      setTransferType("SALE");
      const res = await transferApi.list();
      setTransfers(res.data);
    } catch (err: any) {
      setTransferError(err.response?.data?.detail || "Transfer failed");
    } finally {
      setTransferring(false);
    }
  };

  const resetCheck = () => { setCheckResult(null); setCheckError(""); setTransferError(""); setImei(""); setSuccess(false); };

  return (
    <div>
      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-green-600" />
          <p className="text-sm text-green-700 font-medium">Device transferred to your name successfully!</p>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <Search className="w-5 h-5 text-primary" />
          Step 1: Check Device IMEI
        </h2>
        {checkError && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">{checkError}</div>
        )}
        {!checkResult ? (
          <form onSubmit={handleCheck} className="flex gap-3 max-w-lg">
            <input
              type="text"
              value={imei}
              onChange={(e) => setImei(e.target.value.replace(/\D/g, "").slice(0, 15))}
              placeholder="Enter 15-digit IMEI number"
              maxLength={15}
              className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
            />
            <button type="submit" disabled={checking} className="bg-primary text-white font-semibold py-3 px-6 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2">
              {checking ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
              Check
            </button>
          </form>
        ) : (
          <div>
            {checkResult.status === "not_registered" && (
              <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                <p className="text-sm text-gray-600 font-medium">IMEI <span className="font-mono">{imei}</span> is not registered in the system.</p>
              </div>
            )}
            {checkResult.status === "active" && (
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center gap-2 mb-3">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-sm font-semibold text-green-700">Device is Clean</span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div><span className="text-gray-500">Brand:</span> <span className="font-medium text-gray-800">{checkResult.brand || "N/A"}</span></div>
                  <div><span className="text-gray-500">Model:</span> <span className="font-medium text-gray-800">{checkResult.model || "N/A"}</span></div>
                  <div className="col-span-2">
                    <span className="text-gray-500">Registered:</span> <span className="font-medium text-gray-800">{checkResult.registration_date ? new Date(checkResult.registration_date).toLocaleDateString() : "N/A"}</span>
                  </div>
                </div>
              </div>
            )}
            {(checkResult.status === "stolen" || checkResult.status === "blocked") && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <ShieldAlert className="w-5 h-5 text-red-600" />
                  <span className="text-sm font-semibold text-red-700 uppercase">{checkResult.status} Device</span>
                </div>
                <p className="text-sm text-red-600">{checkResult.message}</p>
              </div>
            )}
            <button onClick={resetCheck} className="mt-4 text-sm text-primary hover:underline">Check another IMEI</button>
          </div>
        )}
      </div>

      {checkResult?.status === "active" && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <ArrowRightLeft className="w-5 h-5 text-primary" />
            Step 2: Transfer to Your Name
          </h2>
          <p className="text-sm text-gray-500 mb-4">This device ({checkResult.brand} {checkResult.model}) will be transferred to your CNIC.</p>
          {transferError && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">{transferError}</div>
          )}
          <form onSubmit={handleTransfer} className="space-y-4 max-w-lg">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Transfer Type</label>
              <select value={transferType} onChange={(e) => setTransferType(e.target.value)} className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors bg-white">
                {TRANSFER_TYPES.map((t) => (<option key={t} value={t}>{t}</option>))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Notes (optional)</label>
              <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Transfer details..." rows={2} className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors resize-none" />
            </div>
            <div className="flex items-center gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-yellow-600 shrink-0" />
              <p className="text-xs text-yellow-700">By proceeding, you confirm that this device is being legally transferred to you.</p>
            </div>
            <button type="submit" disabled={transferring} className="bg-primary text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2">
              {transferring ? <Loader2 className="w-4 h-4 animate-spin" /> : <ArrowRightLeft className="w-4 h-4" />}
              Transfer to My Name
            </button>
          </form>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Transfer History</h2>
        {loadingHistory ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin w-6 h-6 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        ) : (
          <TransferHistory transfers={transfers} />
        )}
      </div>
    </div>
  );
}

// ─── Main Page ───

export default function TransferPage() {
  const role = getUserRole();
  const isShop = role === "shop_keeper" && isShopVerified();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">
          {isShop ? "OTP Transfer (Shopkeeper)" : "Check & Transfer Device"}
        </h1>
        <p className="text-gray-500 mt-1">
          {isShop
            ? "Transfer device ownership with 2-factor OTP verification from both parties"
            : "Check a device IMEI status before transferring ownership to your name"}
        </p>
      </div>

      {isShop ? <ShopOTPTransfer /> : <CitizenTransfer />}
    </div>
  );
}
