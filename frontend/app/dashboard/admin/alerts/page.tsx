"use client";

import { useState, useEffect } from "react";
import { ShieldAlert, CheckCircle, Eye, Loader2 } from "lucide-react";
import { adminApi, PoliceAlertRecord } from "@/lib/api";

export default function PoliceAlertsPage() {
  const [alerts, setAlerts] = useState<PoliceAlertRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "unreviewed" | "reviewed">("unreviewed");
  const [reviewing, setReviewing] = useState<number | null>(null);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const params: { is_reviewed?: boolean } = {};
      if (filter === "unreviewed") params.is_reviewed = false;
      if (filter === "reviewed") params.is_reviewed = true;
      const res = await adminApi.getAlerts(params);
      setAlerts(res.data);
    } catch {
      // silently fail
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [filter]);

  const handleReview = async (alertId: number) => {
    setReviewing(alertId);
    try {
      await adminApi.reviewAlert(alertId);
      await fetchAlerts();
    } catch {
      // silently fail
    } finally {
      setReviewing(null);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <ShieldAlert className="w-6 h-6 text-red-500" />
          <h1 className="text-2xl font-bold text-gray-800">Police Alerts</h1>
        </div>
        <p className="text-gray-500">
          Alerts generated when stolen/blocked devices are checked
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 mb-6">
        {(["unreviewed", "all", "reviewed"] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? "bg-primary text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
          <ShieldAlert className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">No alerts found</p>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`bg-white rounded-xl shadow-sm border p-5 ${
                alert.is_reviewed ? "border-gray-100" : "border-red-200"
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold uppercase ${
                        alert.device_status === "stolen"
                          ? "bg-red-100 text-red-700"
                          : "bg-orange-100 text-orange-700"
                      }`}
                    >
                      {alert.device_status}
                    </span>
                    <span className="text-xs text-gray-400">
                      IMEI: <span className="font-mono">{alert.imei}</span>
                    </span>
                    {alert.is_reviewed && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700">
                        <CheckCircle className="w-3 h-3" /> Reviewed
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm mt-3">
                    <div>
                      <span className="text-gray-400 text-xs block">Checker Name</span>
                      <span className="font-medium text-gray-800">{alert.checker_name}</span>
                    </div>
                    <div>
                      <span className="text-gray-400 text-xs block">CNIC</span>
                      <span className="font-mono text-gray-800">{alert.checker_cnic}</span>
                    </div>
                    <div>
                      <span className="text-gray-400 text-xs block">Phone</span>
                      <span className="font-mono text-gray-800">{alert.checker_phone}</span>
                    </div>
                    <div>
                      <span className="text-gray-400 text-xs block">Role</span>
                      <span className="text-gray-800 capitalize">{alert.checker_role}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 mt-3 text-xs text-gray-400">
                    <span>
                      {new Date(alert.created_at).toLocaleString()}
                    </span>
                    {alert.ip_address && (
                      <span>IP: {alert.ip_address}</span>
                    )}
                  </div>
                </div>

                {!alert.is_reviewed && (
                  <button
                    onClick={() => handleReview(alert.id)}
                    disabled={reviewing === alert.id}
                    className="flex items-center gap-1 px-3 py-2 text-sm font-medium bg-primary text-white rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60"
                  >
                    {reviewing === alert.id ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Eye className="w-4 h-4" />
                    )}
                    Review
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
