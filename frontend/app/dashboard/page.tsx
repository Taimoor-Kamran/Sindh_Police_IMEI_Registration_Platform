"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Smartphone, ArrowRightLeft, AlertTriangle, Plus } from "lucide-react";
import StatsCard from "@/components/StatsCard";
import DeviceTable from "@/components/DeviceTable";
import VerificationBanner from "@/components/VerificationBanner";
import { getUser, isShopKeeper, isShopVerified } from "@/lib/auth";
import { mobileApi, MobileDevice, DeviceStats } from "@/lib/api";

export default function DashboardPage() {
  const user = getUser();
  const [devices, setDevices] = useState<MobileDevice[]>([]);
  const [stats, setStats] = useState<DeviceStats>({ owned_devices: 0, registered_devices: 0, stolen_devices: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [devicesRes, statsRes] = await Promise.all([
          mobileApi.list(),
          mobileApi.getStats(),
        ]);
        setDevices(devicesRes.data);
        setStats(statsRes.data);
      } catch {
        // Stats will show 0 if API fails
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const registerLink = isShopKeeper()
    ? "/dashboard/register-device-shop"
    : "/dashboard/register-device";

  return (
    <div>
      {/* Verification Banner for unverified shop keepers */}
      {isShopKeeper() && !isShopVerified() && <VerificationBanner />}

      {/* Welcome */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">
          Welcome back, {user?.full_name || "User"}
        </h1>
        <p className="text-gray-500 mt-1">
          Manage your registered mobile devices and reports
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
        <StatsCard
          title="Registered Devices"
          value={stats.registered_devices}
          icon={Smartphone}
          color="green"
        />
        <StatsCard
          title="Owned Devices"
          value={stats.owned_devices}
          icon={ArrowRightLeft}
          color="gold"
        />
        <StatsCard
          title="Stolen/Blocked"
          value={stats.stolen_devices}
          icon={AlertTriangle}
          color="red"
        />
      </div>

      {/* My Mobiles */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-800">
            {isShopKeeper() ? "My Registrations" : "My Mobiles"}
          </h2>
          <Link
            href={registerLink}
            className="inline-flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-light transition-colors"
          >
            <Plus className="w-4 h-4" />
            {isShopKeeper() ? "Register for Customer" : "Register New Mobile"}
          </Link>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        ) : devices.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Smartphone className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-gray-600 font-medium mb-2">
              No devices registered yet
            </h3>
            <p className="text-sm text-gray-400 max-w-sm mx-auto">
              Register your mobile devices to protect them against snatching and
              enable ownership transfer.
            </p>
          </div>
        ) : (
          <DeviceTable devices={devices} showOwner={isShopKeeper()} />
        )}
      </div>
    </div>
  );
}
