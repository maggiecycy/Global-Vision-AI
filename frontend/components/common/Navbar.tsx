"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Settings", path: "/settings" },
    { name: "Login", path: "/login" },
  ];

  return (
    <nav className="fixed top-0 w-full bg-zinc-50/80 backdrop-blur-md border-b border-zinc-200 z-50">
      <div className="max-w-6xl mx-auto px-8 h-16 flex items-center justify-between">
        <div className="text-zinc-900 font-serif italic tracking-wider text-lg">
          Global Vision.
        </div>
        <div className="flex gap-8 text-sm tracking-wide">
          {navItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                className={`transition-colors duration-300 ${
                  isActive ? "text-zinc-900 font-medium" : "text-zinc-400 hover:text-zinc-600"
                }`}
              >
                {item.name}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}