"use client";

import { useState, useEffect } from "react";
import { ScrollText, RefreshCw } from "lucide-react";
import { adminApi, AuditLogEntry } from "@/lib/api";

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await adminApi.getAuditLogs({
        action_type: filter || undefined,
        limit: 100,
      });
      setLogs(res.data);
    } catch {
      // Silently fail
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [filter]);

  const actionTypes = [
    "",
    "DEVICE_REGISTERED",
    "DEVICE_REGISTERED_SHOP",
    "DEVICE_TRANSFERRED",
    "DEVICE_BLOCKED",
    "DEVICE_UNBLOCKED",
    "SHOP_APPROVED",
    "SHOP_SUSPENDED",
  ];

  const actionColor: Record<string, string> = {
    DEVICE_REGISTERED: "bg-green-100 text-green-700",
    DEVICE_REGISTERED_SHOP: "bg-yellow-100 text-yellow-700",
    DEVICE_TRANSFERRED: "bg-blue-100 text-blue-700",
    DEVICE_BLOCKED: "bg-red-100 text-red-700",
    DEVICE_UNBLOCKED: "bg-green-100 text-green-700",
    SHOP_APPROVED: "bg-green-100 text-green-700",
    SHOP_SUSPENDED: "bg-red-100 text-red-700",
  };

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <ScrollText className="w-6 h-6 text-primary" />
          <h1 className="text-2xl font-bold text-gray-800">Audit Logs</h1>
        </div>
        <p className="text-gray-500">
          View all system activity and state-changing operations
        </p>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-6">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary text-sm bg-white"
        >
          <option value="">All Actions</option>
          {actionTypes.filter(Boolean).map((t) => (
            <option key={t} value={t}>
              {t.replace(/_/g, " ")}
            </option>
          ))}
        </select>
        <button
          onClick={fetchLogs}
          className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 text-gray-500 ${loading ? "animate-spin" : ""}`} />
        </button>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        ) : logs.length === 0 ? (
          <p className="text-center text-gray-400 py-12">No audit logs found</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Time</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Action</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Description</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">User ID</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">IP</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-xs text-gray-500 whitespace-nowrap">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="py-3 px-4">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                        actionColor[log.action_type] || "bg-gray-100 text-gray-700"
                      }`}>
                        {log.action_type.replace(/_/g, " ")}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-600 max-w-md truncate">
                      {log.description}
                    </td>
                    <td className="py-3 px-4 text-xs text-gray-500">
                      {log.user_id || "-"}
                    </td>
                    <td className="py-3 px-4 text-xs text-gray-400 font-mono">
                      {log.ip_address || "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
