import { useMemo } from "react";
import { useLocation } from "react-router";

export const useQuery = () => {
  const { search } = useLocation();

  return useMemo(() => new URLSearchParams(search), [search]);
};

export const API_URL =
  process.env.REACT_APP_API_URL || "https://localhost:8000";
export const REACT_APP_STRIPE_KEY =
  process.env.REACT_APP_STRIPE_KEY ||
  "pk_test_51MAt6AJU3RVFqD4TZZuEmbyaEWoQDGs06vruWuwLIgUKycVbr7xKg6Xo46D8LOLL7nu6GSKPAiUhiocGeoFyIvKg00VKFbEcSw";
