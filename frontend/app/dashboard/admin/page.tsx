"use client";

import { useState, useEffect } from "react";
import { Users, Smartphone, Store, ShieldAlert, LayoutDashboard, FileText } from "lucide-react";
import StatsCard from "@/components/StatsCard";
import { adminApi, AdminStats } from "@/lib/api";

export default function AdminOverviewPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const res = await adminApi.getStats();
        setStats(res.data);
      } catch {
        // Silently fail
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <LayoutDashboard className="w-6 h-6 text-primary" />
          <h1 className="text-2xl font-bold text-gray-800">Admin Overview</h1>
        </div>
        <p className="text-gray-500">
          System-wide statistics and management dashboard
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <StatsCard
          title="Total Users"
          value={stats?.total_users || 0}
          icon={Users}
          color="blue"
        />
        <StatsCard
          title="Total Devices"
          value={stats?.total_devices || 0}
          icon={Smartphone}
          color="green"
        />
        <StatsCard
          title="Shop Keepers"
          value={stats?.total_shop_keepers || 0}
          icon={Store}
          color="gold"
        />
        <StatsCard
          title="Pending Approvals"
          value={stats?.pending_shop_approvals || 0}
          icon={ShieldAlert}
          color="red"
        />
        <StatsCard
          title="Police Alerts"
          value={stats?.unreviewed_alerts || 0}
          icon={ShieldAlert}
          color="red"
        />
        <StatsCard
          title="Snatching Reports"
          value={stats?.unreviewed_snatch_reports || 0}
          icon={FileText}
          color="red"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">
            Quick Actions
          </h2>
          <div className="space-y-3 mt-4">
            <a
              href="/dashboard/admin/shops"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors border border-gray-100"
            >
              <Store className="w-5 h-5 text-yellow-600" />
              <div>
                <p className="text-sm font-medium text-gray-800">
                  Manage Shop Keepers
                </p>
                <p className="text-xs text-gray-500">
                  {stats?.pending_shop_approvals || 0} pending approvals
                </p>
              </div>
            </a>
            <a
              href="/dashboard/admin/alerts"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors border border-red-100 bg-red-50/30"
            >
              <ShieldAlert className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-sm font-medium text-gray-800">
                  Police Alerts
                </p>
                <p className="text-xs text-gray-500">
                  {stats?.unreviewed_alerts || 0} unreviewed alerts
                </p>
              </div>
            </a>
            <a
              href="/dashboard/admin/snatch-reports"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors border border-red-100 bg-red-50/30"
            >
              <FileText className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-sm font-medium text-gray-800">
                  Snatching Reports
                </p>
                <p className="text-xs text-gray-500">
                  {stats?.unreviewed_snatch_reports || 0} unreviewed reports
                </p>
              </div>
            </a>
            <a
              href="/dashboard/admin/search"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors border border-gray-100"
            >
              <Smartphone className="w-5 h-5 text-primary" />
              <div>
                <p className="text-sm font-medium text-gray-800">
                  Search IMEI
                </p>
                <p className="text-xs text-gray-500">
                  Look up device by IMEI number
                </p>
              </div>
            </a>
            <a
              href="/dashboard/admin/audit"
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors border border-gray-100"
            >
              <ShieldAlert className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-sm font-medium text-gray-800">
                  Audit Logs
                </p>
                <p className="text-xs text-gray-500">
                  View system activity logs
                </p>
              </div>
            </a>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">
            System Summary
          </h2>
          <div className="space-y-4 mt-4">
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm text-gray-500">Blocked Devices</span>
              <span className="text-sm font-semibold text-red-600">
                {stats?.blocked_devices || 0}
              </span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm text-gray-500">Verified Shops</span>
              <span className="text-sm font-semibold text-green-600">
                {(stats?.total_shop_keepers || 0) -
                  (stats?.pending_shop_approvals || 0)}
              </span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm text-gray-500">Total Registered Devices</span>
              <span className="text-sm font-semibold text-primary">
                {stats?.total_devices || 0}
              </span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm text-gray-500">Unreviewed Police Alerts</span>
              <span className="text-sm font-semibold text-red-600">
                {stats?.unreviewed_alerts || 0}
              </span>
            </div>
            <div className="flex items-center justify-between py-2">
              <span className="text-sm text-gray-500">Unreviewed Snatching Reports</span>
              <span className="text-sm font-semibold text-red-600">
                {stats?.unreviewed_snatch_reports || 0}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
