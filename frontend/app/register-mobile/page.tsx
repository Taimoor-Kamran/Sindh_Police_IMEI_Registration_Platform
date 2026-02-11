"use client";

import Link from "next/link";
import { Shield, Smartphone, Store, ChevronRight, ArrowLeft } from "lucide-react";

export default function RegisterMobilePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-primary to-primary-light flex items-center justify-center p-4">
      <div className="w-full max-w-3xl">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center">
              <Shield className="w-7 h-7 text-primary" />
            </div>
            <span className="text-white font-bold text-xl">Sindh Police</span>
          </Link>
          <h1 className="text-3xl font-bold text-white">Register Your Mobile</h1>
          <p className="text-gray-300 mt-2">
            Choose how you want to register your mobile device
          </p>
          <p className="font-urdu text-gray-300 mt-1">
            اپنا موبائل رجسٹر کرنے کا طریقہ منتخب کریں
          </p>
        </div>

        {/* Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Citizen Card */}
          <Link
            href="/register"
            className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all hover:-translate-y-1 group"
          >
            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-primary transition-colors">
              <Smartphone className="w-8 h-8 text-primary group-hover:text-white transition-colors" />
            </div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">
              Citizen Registration
            </h2>
            <p className="text-gray-500 text-sm mb-4">
              Register as an individual citizen to protect your personal mobile
              devices. Track ownership and report incidents.
            </p>
            <p className="font-urdu text-gray-400 text-sm mb-4">
              شہری کے طور پر رجسٹر کریں
            </p>
            <div className="flex items-center text-primary font-medium text-sm group-hover:gap-2 transition-all">
              Register as Citizen
              <ChevronRight className="w-4 h-4 ml-1" />
            </div>
          </Link>

          {/* Shop Keeper Card */}
          <Link
            href="/register-shop"
            className="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all hover:-translate-y-1 group"
          >
            <div className="w-16 h-16 bg-accent/20 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-accent transition-colors">
              <Store className="w-8 h-8 text-yellow-700 group-hover:text-primary transition-colors" />
            </div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">
              Shop Keeper Registration
            </h2>
            <p className="text-gray-500 text-sm mb-4">
              Register as a mobile shop to register devices on behalf of
              customers. Requires shop license verification.
            </p>
            <p className="font-urdu text-gray-400 text-sm mb-4">
              دکاندار کے طور پر رجسٹر کریں
            </p>
            <div className="flex items-center text-yellow-700 font-medium text-sm group-hover:gap-2 transition-all">
              Register as Shop Keeper
              <ChevronRight className="w-4 h-4 ml-1" />
            </div>
          </Link>
        </div>

        {/* Back link */}
        <div className="text-center mt-8">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-gray-300 hover:text-white transition-colors text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}
