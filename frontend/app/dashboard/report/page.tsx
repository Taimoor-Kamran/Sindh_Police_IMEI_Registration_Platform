"use client";

import { useState, useEffect, FormEvent } from "react";
import {
  FileText,
  AlertTriangle,
  Loader2,
  CheckCircle,
  Clock,
  Eye,
} from "lucide-react";
import { snatchReportApi, SnatchReport } from "@/lib/api";

const STATUS_COLORS: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  under_review: "bg-blue-100 text-blue-800",
  resolved: "bg-green-100 text-green-800",
};

export default function ReportPage() {
  const [reports, setReports] = useState<SnatchReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  // Form state
  const [victimCnic, setVictimCnic] = useState("");
  const [deviceImei, setDeviceImei] = useState("");
  const [description, setDescription] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [incidentLocation, setIncidentLocation] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const fetchReports = async () => {
    try {
      const res = await snatchReportApi.list();
      setReports(res.data);
    } catch {
      // silently fail
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!victimCnic.trim()) {
      setError("Please enter the victim's CNIC");
      return;
    }
    if (!deviceImei.trim() || deviceImei.length !== 15) {
      setError("Please enter a valid 15-digit IMEI");
      return;
    }
    if (!description.trim() || description.trim().length < 10) {
      setError("Description must be at least 10 characters");
      return;
    }

    setSubmitting(true);
    try {
      await snatchReportApi.create({
        victim_cnic: victimCnic.trim(),
        device_imei: deviceImei.trim(),
        incident_description: description.trim(),
        incident_date: incidentDate || undefined,
        incident_location: incidentLocation || undefined,
      });
      setSuccess(true);
      setShowForm(false);
      setVictimCnic("");
      setDeviceImei("");
      setDescription("");
      setIncidentDate("");
      setIncidentLocation("");
      fetchReports();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to submit report");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Report Snatching</h1>
        <p className="text-gray-500 mt-1">
          Report snatching incidents for swift police action
        </p>
      </div>

      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-green-600" />
          <p className="text-sm text-green-700 font-medium">
            Report submitted successfully. Police have been notified.
          </p>
        </div>
      )}

      {/* File New Report Button / Form */}
      {!showForm ? (
        <div className="mb-6">
          <button
            onClick={() => { setShowForm(true); setSuccess(false); }}
            className="inline-flex items-center gap-2 bg-red-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
          >
            <FileText className="w-4 h-4" />
            File New Report
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            File Snatching Report
          </h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 max-w-lg">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Victim CNIC *
              </label>
              <input
                type="text"
                value={victimCnic}
                onChange={(e) => setVictimCnic(e.target.value)}
                placeholder="XXXXX-XXXXXXX-X"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Device IMEI *
              </label>
              <input
                type="text"
                value={deviceImei}
                onChange={(e) => setDeviceImei(e.target.value.replace(/\D/g, "").slice(0, 15))}
                placeholder="15-digit IMEI number"
                maxLength={15}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Incident Description *
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe what happened, where, and when..."
                rows={4}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors resize-none"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Incident Date (optional)
                </label>
                <input
                  type="datetime-local"
                  value={incidentDate}
                  onChange={(e) => setIncidentDate(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location (optional)
                </label>
                <input
                  type="text"
                  value={incidentLocation}
                  onChange={(e) => setIncidentLocation(e.target.value)}
                  placeholder="e.g. Saddar, Karachi"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
                />
              </div>
            </div>

            <div className="flex items-center gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <AlertTriangle className="w-4 h-4 text-yellow-600 shrink-0" />
              <p className="text-xs text-yellow-700">
                Filing a false report is a criminal offense. Ensure all information is accurate.
              </p>
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={submitting}
                className="bg-red-600 text-white font-semibold py-2.5 px-6 rounded-lg hover:bg-red-700 transition-colors disabled:opacity-60 flex items-center gap-2"
              >
                {submitting ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <FileText className="w-4 h-4" />
                )}
                Submit Report
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="text-gray-500 font-medium py-2.5 px-6 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Reports List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          My Reports
        </h2>

        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin w-6 h-6 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        ) : reports.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-sm text-gray-400">No reports filed yet</p>
          </div>
        ) : (
          <div className="space-y-4">
            {reports.map((report) => (
              <div
                key={report.id}
                className="p-4 border border-gray-100 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <span className="font-mono text-sm font-medium text-gray-800">
                      IMEI: {report.device_imei}
                    </span>
                    <span className="text-gray-400 mx-2">|</span>
                    <span className="text-sm text-gray-500">
                      Victim: {report.victim_cnic}
                    </span>
                  </div>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      STATUS_COLORS[report.status] || "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {report.status.replace("_", " ")}
                  </span>
                </div>
                <p className="text-sm text-gray-600 line-clamp-2">
                  {report.incident_description}
                </p>
                <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(report.created_at).toLocaleString()}
                  </span>
                  {report.incident_location && (
                    <span>Location: {report.incident_location}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
