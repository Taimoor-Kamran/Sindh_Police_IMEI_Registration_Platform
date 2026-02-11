"use client";

import { useState, useEffect } from "react";
import {
  FileText,
  CheckCircle,
  Clock,
  Loader2,
  Filter,
} from "lucide-react";
import { adminApi, SnatchReport } from "@/lib/api";

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  under_review: "bg-blue-100 text-blue-800",
  resolved: "bg-green-100 text-green-800",
};

type FilterType = "unreviewed" | "reviewed" | "all";

export default function AdminSnatchReportsPage() {
  const [reports, setReports] = useState<SnatchReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<FilterType>("unreviewed");
  const [reviewingId, setReviewingId] = useState<number | null>(null);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const params: { is_reviewed?: boolean } = {};
      if (filter === "unreviewed") params.is_reviewed = false;
      if (filter === "reviewed") params.is_reviewed = true;
      const res = await adminApi.listSnatchReports(params);
      setReports(res.data);
    } catch {
      // silently fail
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, [filter]);

  const handleReview = async (reportId: number) => {
    setReviewingId(reportId);
    try {
      await adminApi.reviewSnatchReport(reportId);
      fetchReports();
    } catch {
      // silently fail
    } finally {
      setReviewingId(null);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <FileText className="w-6 h-6 text-red-500" />
          <h1 className="text-2xl font-bold text-gray-800">
            Snatching Reports
          </h1>
        </div>
        <p className="text-gray-500">
          Review and manage snatching incident reports from citizens
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 mb-6">
        {(["unreviewed", "reviewed", "all"] as FilterType[]).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? "bg-primary text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {f === "unreviewed"
              ? "Unreviewed"
              : f === "reviewed"
              ? "Reviewed"
              : "All Reports"}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
        </div>
      ) : reports.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
          <p className="text-sm text-gray-400">
            No {filter === "all" ? "" : filter} reports found
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {reports.map((report) => (
            <div
              key={report.id}
              className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="text-sm font-bold text-gray-800">
                      Report #{report.id}
                    </span>
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        STATUS_COLORS[report.status] || "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {report.status.replace("_", " ")}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-gray-400">
                    <Clock className="w-3 h-3" />
                    {new Date(report.created_at).toLocaleString()}
                  </div>
                </div>
                {!report.is_reviewed && (
                  <button
                    onClick={() => handleReview(report.id)}
                    disabled={reviewingId === report.id}
                    className="bg-primary text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center gap-2"
                  >
                    {reviewingId === report.id ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <CheckCircle className="w-4 h-4" />
                    )}
                    Mark as Reviewed
                  </button>
                )}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
                <div>
                  <span className="text-xs text-gray-500 block">Reporter</span>
                  <span className="text-sm font-medium text-gray-800">
                    {report.reporter_name}
                  </span>
                  <span className="text-xs text-gray-400 block">
                    {report.reporter_cnic} | {report.reporter_phone}
                  </span>
                </div>
                <div>
                  <span className="text-xs text-gray-500 block">Victim CNIC</span>
                  <span className="text-sm font-medium text-gray-800">
                    {report.victim_cnic}
                  </span>
                </div>
                <div>
                  <span className="text-xs text-gray-500 block">Device IMEI</span>
                  <span className="text-sm font-mono font-medium text-gray-800">
                    {report.device_imei}
                  </span>
                  {report.mobile_id && (
                    <span className="text-xs text-green-600 block">
                      Registered in system
                    </span>
                  )}
                </div>
                {report.incident_location && (
                  <div>
                    <span className="text-xs text-gray-500 block">Location</span>
                    <span className="text-sm font-medium text-gray-800">
                      {report.incident_location}
                    </span>
                  </div>
                )}
              </div>

              <div className="p-3 bg-gray-50 rounded-lg">
                <span className="text-xs text-gray-500 block mb-1">
                  Incident Description
                </span>
                <p className="text-sm text-gray-700">
                  {report.incident_description}
                </p>
              </div>

              {report.is_reviewed && report.reviewed_at && (
                <div className="mt-3 text-xs text-gray-400">
                  Reviewed on {new Date(report.reviewed_at).toLocaleString()}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
