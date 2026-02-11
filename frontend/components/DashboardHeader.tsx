"use client";

import { useRouter } from "next/navigation";
import { LogOut, Menu, Shield } from "lucide-react";
import { authApi } from "@/lib/api";
import { logout as clearAuth, getUser } from "@/lib/auth";

interface DashboardHeaderProps {
  onMenuToggle: () => void;
}

export default function DashboardHeader({ onMenuToggle }: DashboardHeaderProps) {
  const router = useRouter();
  const user = getUser();

  const handleLogout = async () => {
    try {
      await authApi.logout();
    } catch {
      // Proceed with local logout even if API call fails
    }
    clearAuth();
    router.push("/login");
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-4 lg:px-6 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuToggle}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100"
          >
            <Menu className="w-5 h-5 text-gray-600" />
          </button>
          <div className="hidden lg:flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary" />
            <span className="text-sm font-semibold text-primary">
              Dashboard
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-sm font-medium text-gray-800">
              {user?.full_name || "User"}
            </p>
            <p className="text-xs text-gray-500 capitalize">
              {user?.role || "citizen"}
            </p>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
}
