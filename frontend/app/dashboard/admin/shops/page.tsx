"use client";

import { useState, useEffect } from "react";
import { Store, CheckCircle, XCircle, Loader2 } from "lucide-react";
import RoleBadge from "@/components/RoleBadge";
import { adminApi } from "@/lib/api";

interface ShopKeeper {
  id: number;
  full_name: string;
  username: string;
  cnic: string;
  mobile: string;
  email: string;
  shop_license_number: string | null;
  is_shop_verified: boolean;
  is_active: boolean;
  created_at: string;
}

export default function ManageShopsPage() {
  const [shops, setShops] = useState<ShopKeeper[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [filter, setFilter] = useState<"all" | "pending" | "verified">("all");

  const fetchShops = async () => {
    try {
      const verified =
        filter === "pending" ? false : filter === "verified" ? true : undefined;
      const res = await adminApi.listShopKeepers(verified);
      setShops(res.data);
    } catch {
      // Silently fail
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    fetchShops();
  }, [filter]);

  const handleApprove = async (userId: number) => {
    setActionLoading(userId);
    try {
      await adminApi.approveShop(userId);
      await fetchShops();
    } catch {
      // Silently fail
    } finally {
      setActionLoading(null);
    }
  };

  const handleSuspend = async (userId: number) => {
    setActionLoading(userId);
    try {
      await adminApi.suspendShop(userId);
      await fetchShops();
    } catch {
      // Silently fail
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Store className="w-6 h-6 text-yellow-600" />
          <h1 className="text-2xl font-bold text-gray-800">Manage Shop Keepers</h1>
        </div>
        <p className="text-gray-500">
          Approve or suspend shop keeper accounts
        </p>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-6">
        {(["all", "pending", "verified"] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? "bg-primary text-white"
                : "bg-white border border-gray-200 text-gray-600 hover:bg-gray-50"
            }`}
          >
            {f === "all" ? "All" : f === "pending" ? "Pending" : "Verified"}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full" />
          </div>
        ) : shops.length === 0 ? (
          <p className="text-center text-gray-400 py-12">
            No shop keepers found
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Name</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">CNIC</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">License #</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Registered</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">Actions</th>
                </tr>
              </thead>
              <tbody>
                {shops.map((shop) => (
                  <tr key={shop.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4">
                      <p className="font-medium text-gray-800">{shop.full_name}</p>
                      <p className="text-xs text-gray-400">{shop.email}</p>
                    </td>
                    <td className="py-3 px-4 font-mono text-xs">{shop.cnic}</td>
                    <td className="py-3 px-4 text-xs">{shop.shop_license_number || "-"}</td>
                    <td className="py-3 px-4">
                      {shop.is_shop_verified ? (
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-green-700 bg-green-100 px-2 py-0.5 rounded">
                          <CheckCircle className="w-3 h-3" />
                          Verified
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-yellow-700 bg-yellow-100 px-2 py-0.5 rounded">
                          Pending
                        </span>
                      )}
                      {!shop.is_active && (
                        <span className="ml-1 inline-flex items-center text-xs font-medium text-red-700 bg-red-100 px-2 py-0.5 rounded">
                          Suspended
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-xs text-gray-500">
                      {new Date(shop.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        {!shop.is_shop_verified && shop.is_active && (
                          <button
                            onClick={() => handleApprove(shop.id)}
                            disabled={actionLoading === shop.id}
                            className="inline-flex items-center gap-1 px-3 py-1.5 bg-green-50 text-green-700 rounded-lg text-xs font-medium hover:bg-green-100 transition-colors disabled:opacity-50"
                          >
                            {actionLoading === shop.id ? (
                              <Loader2 className="w-3 h-3 animate-spin" />
                            ) : (
                              <CheckCircle className="w-3 h-3" />
                            )}
                            Approve
                          </button>
                        )}
                        {shop.is_active && (
                          <button
                            onClick={() => handleSuspend(shop.id)}
                            disabled={actionLoading === shop.id}
                            className="inline-flex items-center gap-1 px-3 py-1.5 bg-red-50 text-red-700 rounded-lg text-xs font-medium hover:bg-red-100 transition-colors disabled:opacity-50"
                          >
                            {actionLoading === shop.id ? (
                              <Loader2 className="w-3 h-3 animate-spin" />
                            ) : (
                              <XCircle className="w-3 h-3" />
                            )}
                            Suspend
                          </button>
                        )}
                      </div>
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
