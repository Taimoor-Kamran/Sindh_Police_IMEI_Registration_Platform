"use client";

import { useState, useEffect } from "react";
import {
  BarChart3,
  Smartphone,
  ArrowRightLeft,
  ArrowDownLeft,
  ArrowUpRight,
  Store,
} from "lucide-react";
import StatsCard from "@/components/StatsCard";
import {
  reportsApi,
  MobileDevice,
  TransferRecord,
  CitizenReportStats,
  ShopReportStats,
} from "@/lib/api";
import { getUserRole } from "@/lib/auth";

function CitizenReports() {
  const [stats, setStats] = useState<CitizenReportStats | null>(null);
  const [devices, setDevices] = useState<MobileDevice[]>([]);
  const [transfers, setTransfers] = useState<TransferRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      reportsApi.citizenStats(),
      reportsApi.citizenDevices(),
      reportsApi.citizenTransfers(),
    ])
      .then(([statsRes, devicesRes, transfersRes]) => {
        setStats(statsRes.data);
        setDevices(devicesRes.data);
        setTransfers(transfersRes.data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
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
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
        <StatsCard title="Devices Owned" value={stats?.total_owned || 0} icon={Smartphone} color="green" />
        <StatsCard title="Transferred Away" value={stats?.total_transferred_away || 0} icon={ArrowUpRight} color="red" />
        <StatsCard title="Received" value={stats?.total_received || 0} icon={ArrowDownLeft} color="blue" />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">My Devices</h2>
        {devices.length === 0 ? (
          <p className="text-sm text-gray-400 py-4 text-center">No devices owned</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100 text-left text-gray-500">
                  <th className="pb-3 font-medium">IMEI</th>
                  <th className="pb-3 font-medium">Brand</th>
                  <th className="pb-3 font-medium">Model</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium">Registered</th>
                </tr>
              </thead>
              <tbody>
                {devices.map((d) => (
                  <tr key={d.id} className="border-b border-gray-50">
                    <td className="py-3 font-mono">{d.imei}</td>
                    <td className="py-3">{d.brand || "-"}</td>
                    <td className="py-3">{d.model || "-"}</td>
                    <td className="py-3">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        d.status === "active" ? "bg-green-100 text-green-800" :
                        d.status === "stolen" ? "bg-red-100 text-red-800" :
                        "bg-gray-100 text-gray-800"
                      }`}>{d.status}</span>
                    </td>
                    <td className="py-3 text-gray-500">{new Date(d.registration_date).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Transfer History</h2>
        {transfers.length === 0 ? (
          <p className="text-sm text-gray-400 py-4 text-center">No transfers</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100 text-left text-gray-500">
                  <th className="pb-3 font-medium">IMEI</th>
                  <th className="pb-3 font-medium">From</th>
                  <th className="pb-3 font-medium">To</th>
                  <th className="pb-3 font-medium">Type</th>
                  <th className="pb-3 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {transfers.map((t) => (
                  <tr key={t.id} className="border-b border-gray-50">
                    <td className="py-3 font-mono">{t.imei}</td>
                    <td className="py-3">{t.old_owner_cnic}</td>
                    <td className="py-3">{t.new_owner_cnic}</td>
                    <td className="py-3">
                      <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{t.transfer_type}</span>
                    </td>
                    <td className="py-3 text-gray-500">{new Date(t.transfer_date).toLocaleDateString()}</td>
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

function ShopReports() {
  const [stats, setStats] = useState<ShopReportStats | null>(null);
  const [devices, setDevices] = useState<MobileDevice[]>([]);
  const [transfers, setTransfers] = useState<TransferRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      reportsApi.shopStats(),
      reportsApi.shopDevices(),
      reportsApi.shopTransfers(),
    ])
      .then(([statsRes, devicesRes, transfersRes]) => {
        setStats(statsRes.data);
        setDevices(devicesRes.data);
        setTransfers(transfersRes.data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
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
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <StatsCard title="Devices Registered" value={stats?.total_registered || 0} icon={Store} color="green" />
        <StatsCard title="Transfers Performed" value={stats?.total_transferred || 0} icon={ArrowRightLeft} color="blue" />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Registered Devices</h2>
        {devices.length === 0 ? (
          <p className="text-sm text-gray-400 py-4 text-center">No devices registered yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100 text-left text-gray-500">
                  <th className="pb-3 font-medium">IMEI</th>
                  <th className="pb-3 font-medium">Brand</th>
                  <th className="pb-3 font-medium">Model</th>
                  <th className="pb-3 font-medium">Owner CNIC</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {devices.map((d) => (
                  <tr key={d.id} className="border-b border-gray-50">
                    <td className="py-3 font-mono">{d.imei}</td>
                    <td className="py-3">{d.brand || "-"}</td>
                    <td className="py-3">{d.model || "-"}</td>
                    <td className="py-3">{d.current_owner_cnic}</td>
                    <td className="py-3">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        d.status === "active" ? "bg-green-100 text-green-800" :
                        d.status === "stolen" ? "bg-red-100 text-red-800" :
                        "bg-gray-100 text-gray-800"
                      }`}>{d.status}</span>
                    </td>
                    <td className="py-3 text-gray-500">{new Date(d.registration_date).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Transfers Performed</h2>
        {transfers.length === 0 ? (
          <p className="text-sm text-gray-400 py-4 text-center">No transfers performed</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100 text-left text-gray-500">
                  <th className="pb-3 font-medium">IMEI</th>
                  <th className="pb-3 font-medium">From</th>
                  <th className="pb-3 font-medium">To</th>
                  <th className="pb-3 font-medium">Type</th>
                  <th className="pb-3 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {transfers.map((t) => (
                  <tr key={t.id} className="border-b border-gray-50">
                    <td className="py-3 font-mono">{t.imei}</td>
                    <td className="py-3">{t.old_owner_cnic}</td>
                    <td className="py-3">{t.new_owner_cnic}</td>
                    <td className="py-3">
                      <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{t.transfer_type}</span>
                    </td>
                    <td className="py-3 text-gray-500">{new Date(t.transfer_date).toLocaleDateString()}</td>
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

export default function ReportsPage() {
  const role = getUserRole();
  const isShop = role === "shop_keeper";

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <BarChart3 className="w-6 h-6 text-primary" />
          <h1 className="text-2xl font-bold text-gray-800">
            {isShop ? "Shop Reports" : "My Reports"}
          </h1>
        </div>
        <p className="text-gray-500">
          {isShop
            ? "View your shop's device registration and transfer activity"
            : "View your device ownership and transfer activity"}
        </p>
      </div>

      {isShop ? <ShopReports /> : <CitizenReports />}
    </div>
  );
}
