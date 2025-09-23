import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    rules: {},
    root: process.cwd(),
  },
};

export default nextConfig;
