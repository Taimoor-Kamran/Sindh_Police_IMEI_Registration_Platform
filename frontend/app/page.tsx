import Link from "next/link";
import {
  Shield,
  Smartphone,
  Users,
  FileText,
  Siren,
  User,
  ChevronRight,
} from "lucide-react";

const features = [
  {
    icon: Smartphone,
    title: "Device Registration",
    description: "Secure your mobile devices with official registration",
  },
  {
    icon: Users,
    title: "Ownership Transfer",
    description: "Legally transfer device ownership with proper documentation",
  },
  {
    icon: FileText,
    title: "Report Incidents",
    description: "Quick reporting system for snatching incidents",
  },
  {
    icon: Siren,
    title: "Police Action",
    description: "Direct connection to Sindh Police for swift response",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-primary text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center">
                <Shield className="w-7 h-7 text-primary" />
              </div>
              <div>
                <h1 className="font-bold text-lg leading-tight">
                  Sindh Police
                </h1>
                <p className="text-xs text-gray-300">
                  IMEI Registration Platform
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-urdu text-lg leading-relaxed">سندھ پولیس</p>
              <p className="font-urdu text-xs text-gray-300">
                آئی ایم ای آئی رجسٹریشن
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary via-primary to-primary-light text-white py-20 lg:py-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 mb-6">
            <Shield className="w-4 h-4 text-accent" />
            <span className="text-sm font-medium">
              Powered by Sindh Police Guidance
            </span>
          </div>

          <h2 className="text-4xl lg:text-5xl font-bold mb-4 leading-tight">
            Mobile Snatching
            <br />
            <span className="text-accent">Prevention Platform</span>
          </h2>

          <p className="font-urdu text-xl text-gray-200 mb-4">
            سندھ پولیس کی رہنمائی میں
          </p>

          <p className="text-lg text-gray-300 max-w-2xl mx-auto mb-10">
            Register your mobile devices, transfer ownership securely, and
            report snatching incidents for swift police action.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register-mobile"
              className="inline-flex items-center justify-center gap-2 bg-accent text-primary font-semibold px-8 py-4 rounded-lg hover:bg-accent-light transition-colors shadow-lg"
            >
              <User className="w-5 h-5" />
              Register Your Mobile
              <ChevronRight className="w-4 h-4" />
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center gap-2 bg-white/10 text-white font-semibold px-8 py-4 rounded-lg hover:bg-white/20 transition-colors border border-white/30"
            >
              <Shield className="w-5 h-5" />
              Police Portal
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 lg:py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-gray-800 mb-3">
              Platform Features
            </h3>
            <p className="text-gray-500 max-w-xl mx-auto">
              A comprehensive system for mobile device registration and
              protection under Sindh Police
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <div
                  key={feature.title}
                  className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary/20 transition-all group"
                >
                  <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-white transition-colors">
                    <Icon className="w-6 h-6 text-primary group-hover:text-white transition-colors" />
                  </div>
                  <h4 className="font-semibold text-gray-800 mb-2">
                    {feature.title}
                  </h4>
                  <p className="text-sm text-gray-500">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-primary text-white py-8 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                <Shield className="w-5 h-5 text-primary" />
              </div>
              <span className="text-sm font-medium">
                Sindh Police IMEI Registration Platform
              </span>
            </div>
            <p className="text-xs text-gray-400">
              &copy; 2024 Sindh Police. All rights reserved.
            </p>
            <p className="font-urdu text-sm text-gray-300">
              سندھ پولیس - عوام کی خدمت میں
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
