import { useQuery } from "@tanstack/react-query";
import { getDashboardStatistics } from "../services/dashboard";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard-statistics"],

    queryFn: getDashboardStatistics,

    staleTime: 30_000,

    refetchInterval: 30_000,
  });
}
