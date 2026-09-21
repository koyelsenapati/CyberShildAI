import {
  Bell,
  Menu,
  Search,
  ShieldCheck,
} from "lucide-react";

interface TopbarProps {
  onMenuClick: () => void;
}

export default function Topbar({ onMenuClick }: TopbarProps) {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-white/10 bg-[#0B0F17]/95 px-4 backdrop-blur md:px-6">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="rounded-lg p-2 text-gray-400 transition hover:bg-white/5 hover:text-white lg:hidden"
          aria-label="Open navigation"
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="hidden items-center gap-2 lg:flex">
          <ShieldCheck className="h-5 w-5 text-[#00F0FF]" />

          <span className="text-sm font-medium text-gray-300">
            Security Operations Center
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2 md:gap-4">
        <div className="hidden items-center gap-2 rounded-lg border border-white/10 bg-[#111827] px-3 py-2 md:flex">
          <Search className="h-4 w-4 text-gray-500" />

          <input
            type="search"
            placeholder="Search security data..."
            className="w-48 bg-transparent text-xs text-white outline-none placeholder:text-gray-600"
          />

          <kbd className="rounded border border-white/10 px-1.5 py-0.5 text-[10px] text-gray-500">
            /
          </kbd>
        </div>

        <button
          className="relative rounded-lg p-2 text-gray-400 transition hover:bg-white/5 hover:text-white"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />

          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-[#EF4444]" />
        </button>

        <div className="h-8 w-px bg-white/10" />

        <button className="flex items-center gap-2 rounded-lg p-1.5 transition hover:bg-white/5">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#00F0FF]/10 text-xs font-semibold text-[#00F0FF]">
            KS
          </div>

          <div className="hidden text-left sm:block">
            <p className="text-xs font-medium text-white">
              Security Analyst
            </p>

            <p className="text-[10px] text-gray-500">
              Administrator
            </p>
          </div>
        </button>
      </div>
    </header>
  );
}
