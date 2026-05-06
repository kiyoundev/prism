import "server-only";

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

export const env = {
  FASTAPI_URL: requireEnv("FASTAPI_URL"),
  INTERNAL_API_KEY: requireEnv("INTERNAL_API_KEY"),
};
