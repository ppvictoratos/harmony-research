import { useEffect, useState } from "react";

export type Route =
  | { page: "evidence" }
  | { page: "studies" }
  | { page: "study"; id: number };

export function parseHash(hash: string): Route {
  const study = hash.match(/^#\/studies\/(\d+)$/);
  if (study) return { page: "study", id: Number(study[1]) };
  if (hash.startsWith("#/studies")) return { page: "studies" };
  return { page: "evidence" };
}

export function useHashRoute(): Route {
  const [route, setRoute] = useState(() => parseHash(window.location.hash));
  useEffect(() => {
    const onChange = () => {
      setRoute(parseHash(window.location.hash));
      window.scrollTo({ top: 0 });
    };
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return route;
}
