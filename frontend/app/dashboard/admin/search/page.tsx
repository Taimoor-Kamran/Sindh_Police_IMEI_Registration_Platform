"use client";

import { useState, FormEvent } from "react";
import { Search, Smartphone, ShieldAlert, ShieldCheck, Loader2 } from "lucide-react";
import { adminApi, MobileDevice } from "@/lib/api";

export default function IMEISearchPage() {
  const [imei, setImei] = useState("");
  const [device, setDevice] = useState<MobileDevice | null>(null);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    if (!imei.trim()) return;

    setLoading(true);
    setError("");
    setDevice(null);
    setSearched(true);

    try {
      const res = await adminApi.searchImei(imei.trim());
      setDevice(res.data);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError("No device found with this IMEI");
      } else {
        setError(err.response?.data?.detail || "Search failed");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBlock = async () => {
    if (!device) return;
    setActionLoading(true);
    try {
      const res = await adminApi.blockDevice(device.id);
      setDevice(res.data);
    } catch {
      // Silently fail
    } finally {
      setActionLoading(false);
    }
  };

  const handleUnblock = async () => {
    if (!device) return;
    setActionLoading(true);
    try {
      const res = await adminApi.unblockDevice(device.id);
      setDevice(res.data);
    } catch {
      // Silently fail
    } finally {
      setActionLoading(false);
    }
  };

  const statusColor: Record<string, string> = {
    active: "text-green-700 bg-green-100",
    stolen: "text-red-700 bg-red-100",
    blocked: "text-gray-700 bg-gray-200",
  };

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Search className="w-6 h-6 text-primary" />
          <h1 className="text-2xl font-bold text-gray-800">IMEI Search</h1>
        </div>
        <p className="text-gray-500">
          Look up a device by IMEI number and manage its status
        </p>
      </div>

      {/* Search Form */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <form onSubmit={handleSearch} className="flex gap-3 max-w-lg">
          <input
            type="text"
            value={imei}
            onChange={(e) => setImei(e.target.value.replace(/\D/g, ""))}
            maxLength={15}
            placeholder="Enter 15-digit IMEI number"
            className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors font-mono tracking-wider"
          />
          <button
            type="submit"
            disabled={loading || imei.length < 15}
            className="bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Search className="w-5 h-5" />
            )}
            Search
          </button>
        </form>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
          <Smartphone className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">{error}</p>
        </div>
      )}

      {/* Result */}
      {device && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-800">Device Details</h2>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColor[device.status] || "bg-gray-100 text-gray-700"}`}>
              {device.status.toUpperCase()}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="space-y-3">
              <div>
                <p className="text-xs text-gray-400">IMEI</p>
                <p className="font-mono font-medium text-gray-800">{device.imei}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Mobile Number</p>
                <p className="text-gray-800">{device.mobile_number}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Brand / Model</p>
                <p className="text-gray-800">
                  {device.brand || "Unknown"} {device.model ? `/ ${device.model}` : ""}
                </p>
              </div>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-xs text-gray-400">Current Owner CNIC</p>
                <p className="font-mono text-gray-800">{device.current_owner_cnic}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Registration Type</p>
                <p className="text-gray-800">{device.registration_type}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Registration Date</p>
                <p className="text-gray-800">
                  {new Date(device.registration_date).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>

          {device.notes && (
            <div className="mb-6">
              <p className="text-xs text-gray-400">Notes</p>
              <p className="text-sm text-gray-600">{device.notes}</p>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t border-gray-100">
            {device.status !== "blocked" ? (
              <button
                onClick={handleBlock}
                disabled={actionLoading}
                className="inline-flex items-center gap-2 px-4 py-2 bg-red-50 text-red-700 rounded-lg text-sm font-medium hover:bg-red-100 transition-colors disabled:opacity-50"
              >
                {actionLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <ShieldAlert className="w-4 h-4" />
                )}
                Block Device
              </button>
            ) : (
              <button
                onClick={handleUnblock}
                disabled={actionLoading}
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-lg text-sm font-medium hover:bg-green-100 transition-colors disabled:opacity-50"
              >
                {actionLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <ShieldCheck className="w-4 h-4" />
                )}
                Unblock Device
              </button>
            )}
          </div>
        </div>
      )}

      {/* Empty state */}
      {!device && !error && searched && !loading && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
          <p className="text-gray-400">No results</p>
        </div>
      )}
    </div>
  );
}
