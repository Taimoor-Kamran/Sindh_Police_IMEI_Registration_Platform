"use client";

import { useState, useEffect } from "react";
import { User, Mail, Phone, CreditCard, Shield, Loader2 } from "lucide-react";
import { userApi } from "@/lib/api";
import { getUser } from "@/lib/auth";

interface ProfileData {
  id: number;
  full_name: string;
  cnic: string;
  mobile: string;
  email: string;
  username: string;
  role: string;
  created_at: string;
  is_active: boolean;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const localUser = getUser();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await userApi.getProfile();
        setProfile(response.data);
      } catch {
        // Fallback to local user data
        if (localUser) {
          setProfile({
            id: localUser.id,
            full_name: localUser.full_name,
            cnic: "---",
            mobile: "---",
            email: "---",
            username: localUser.username,
            role: localUser.role,
            created_at: new Date().toISOString(),
            is_active: true,
          });
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="text-center py-20 text-gray-500">
        Unable to load profile
      </div>
    );
  }

  const infoItems = [
    { icon: User, label: "Full Name", value: profile.full_name },
    { icon: CreditCard, label: "CNIC", value: profile.cnic },
    { icon: Phone, label: "Mobile", value: profile.mobile },
    { icon: Mail, label: "Email", value: profile.email },
    { icon: User, label: "Username", value: profile.username },
    { icon: Shield, label: "Role", value: profile.role },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">My Profile</h1>
        <p className="text-gray-500 mt-1">View and manage your account details</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        {/* Profile Header */}
        <div className="bg-gradient-to-r from-primary to-primary-light p-6">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center text-primary font-bold text-xl">
              {profile.full_name.charAt(0).toUpperCase()}
            </div>
            <div className="text-white">
              <h2 className="text-xl font-bold">{profile.full_name}</h2>
              <p className="text-gray-200 text-sm capitalize">{profile.role}</p>
            </div>
          </div>
        </div>

        {/* Profile Info */}
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {infoItems.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.label}
                  className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg"
                >
                  <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                    <Icon className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">{item.label}</p>
                    <p className="text-sm font-medium text-gray-800">
                      {item.value}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-6 pt-4 border-t border-gray-100">
            <p className="text-xs text-gray-400">
              Member since{" "}
              {new Date(profile.created_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
