"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Shield, Eye, EyeOff, Loader2 } from "lucide-react";
import { authApi, RegisterData } from "@/lib/api";
import { setToken, setUser } from "@/lib/auth";

interface FormErrors {
  full_name?: string;
  cnic?: string;
  mobile?: string;
  email?: string;
  username?: string;
  password?: string;
  confirm_password?: string;
  general?: string;
}

export default function RegisterPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [form, setForm] = useState({
    full_name: "",
    cnic: "",
    mobile: "",
    email: "",
    username: "",
    password: "",
    confirm_password: "",
  });

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (form.full_name.trim().length < 3) {
      newErrors.full_name = "Full name must be at least 3 characters";
    }

    if (!/^\d{5}-\d{7}-\d$/.test(form.cnic)) {
      newErrors.cnic = "CNIC must be in format XXXXX-XXXXXXX-X";
    }

    if (!/^03\d{9}$/.test(form.mobile)) {
      newErrors.mobile = "Mobile must start with 03 and be 11 digits";
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      newErrors.email = "Please enter a valid email address";
    }

    if (form.username.length < 4 || !/^[a-zA-Z0-9_]+$/.test(form.username)) {
      newErrors.username = "Username must be at least 4 alphanumeric characters";
    }

    if (form.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    } else if (!/[A-Z]/.test(form.password)) {
      newErrors.password = "Password must include an uppercase letter";
    } else if (!/[a-z]/.test(form.password)) {
      newErrors.password = "Password must include a lowercase letter";
    } else if (!/\d/.test(form.password)) {
      newErrors.password = "Password must include a number";
    }

    if (form.password !== form.confirm_password) {
      newErrors.confirm_password = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    setErrors({});

    try {
      const data: RegisterData = {
        full_name: form.full_name,
        cnic: form.cnic,
        mobile: form.mobile,
        email: form.email,
        username: form.username,
        password: form.password,
      };

      const response = await authApi.register(data);
      const { token, user_id } = response.data;

      setToken(token);
      setUser({
        id: user_id,
        username: form.username,
        full_name: form.full_name,
        role: "citizen",
      });

      router.push("/dashboard");
    } catch (err: any) {
      const message =
        err.response?.data?.detail || "Registration failed. Please try again.";
      setErrors({ general: message });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    if (errors[field as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-primary to-primary-light flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center">
              <Shield className="w-7 h-7 text-primary" />
            </div>
            <span className="text-white font-bold text-xl">Sindh Police</span>
          </Link>
          <h1 className="text-2xl font-bold text-white">
            Mobile Owner Registration
          </h1>
          <p className="text-gray-300 mt-1 text-sm">
            Create your account to register your devices
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {errors.general && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
              {errors.general}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Full Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              <input
                type="text"
                value={form.full_name}
                onChange={(e) => handleChange("full_name", e.target.value)}
                placeholder="Enter your full name"
                className={`w-full px-4 py-3 rounded-lg border ${
                  errors.full_name ? "border-red-400" : "border-gray-300"
                } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
              />
              {errors.full_name && (
                <p className="text-xs text-red-500 mt-1">{errors.full_name}</p>
              )}
            </div>

            {/* CNIC */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                CNIC Number
              </label>
              <input
                type="text"
                value={form.cnic}
                onChange={(e) => handleChange("cnic", e.target.value)}
                placeholder="XXXXX-XXXXXXX-X"
                maxLength={15}
                className={`w-full px-4 py-3 rounded-lg border ${
                  errors.cnic ? "border-red-400" : "border-gray-300"
                } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
              />
              {errors.cnic && (
                <p className="text-xs text-red-500 mt-1">{errors.cnic}</p>
              )}
            </div>

            {/* Mobile */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Mobile Number
              </label>
              <input
                type="tel"
                value={form.mobile}
                onChange={(e) => handleChange("mobile", e.target.value)}
                placeholder="03XX-XXXXXXX"
                maxLength={11}
                className={`w-full px-4 py-3 rounded-lg border ${
                  errors.mobile ? "border-red-400" : "border-gray-300"
                } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
              />
              {errors.mobile && (
                <p className="text-xs text-red-500 mt-1">{errors.mobile}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => handleChange("email", e.target.value)}
                placeholder="your.email@example.com"
                className={`w-full px-4 py-3 rounded-lg border ${
                  errors.email ? "border-red-400" : "border-gray-300"
                } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
              />
              {errors.email && (
                <p className="text-xs text-red-500 mt-1">{errors.email}</p>
              )}
            </div>

            {/* Username */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <input
                type="text"
                value={form.username}
                onChange={(e) => handleChange("username", e.target.value)}
                placeholder="Choose a username"
                className={`w-full px-4 py-3 rounded-lg border ${
                  errors.username ? "border-red-400" : "border-gray-300"
                } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
              />
              {errors.username && (
                <p className="text-xs text-red-500 mt-1">{errors.username}</p>
              )}
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={(e) => handleChange("password", e.target.value)}
                  placeholder="Minimum 8 characters"
                  className={`w-full px-4 py-3 pr-12 rounded-lg border ${
                    errors.password ? "border-red-400" : "border-gray-300"
                  } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="text-xs text-red-500 mt-1">{errors.password}</p>
              )}
            </div>

            {/* Confirm Password */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password
              </label>
              <div className="relative">
                <input
                  type={showConfirm ? "text" : "password"}
                  value={form.confirm_password}
                  onChange={(e) =>
                    handleChange("confirm_password", e.target.value)
                  }
                  placeholder="Re-enter your password"
                  className={`w-full px-4 py-3 pr-12 rounded-lg border ${
                    errors.confirm_password
                      ? "border-red-400"
                      : "border-gray-300"
                  } focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors`}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirm(!showConfirm)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showConfirm ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.confirm_password && (
                <p className="text-xs text-red-500 mt-1">
                  {errors.confirm_password}
                </p>
              )}
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary text-white font-semibold py-3 rounded-lg hover:bg-primary-light transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Registering...
                </>
              ) : (
                "Register"
              )}
            </button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            Already have an account?{" "}
            <Link
              href="/login"
              className="text-primary font-medium hover:underline"
            >
              Login here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
