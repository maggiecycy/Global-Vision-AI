/**
 * 前端 API 通讯层：统一 BASE_URL、Content-Type 与错误处理
 */

const BASE_URL =
  (typeof process !== "undefined" && process.env?.NEXT_PUBLIC_API_BASE_URL) ||
  "http://127.0.0.1:8000/api/v1";

const DEFAULT_HEADERS: HeadersInit = {
  "Content-Type": "application/json",
};

/** 后端返回的错误结构（FastAPI 常见格式） */
interface ApiErrorDetail {
  detail?: string | { msg?: string; message?: string }[];
}

/**
 * 统一请求封装：检查 res.ok，失败时解析 detail 并抛出自定义 Error
 */
export async function apiRequest<T = unknown>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = path.startsWith("http") ? path : `${BASE_URL.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
  const res = await fetch(url, {
    ...options,
    headers: { ...DEFAULT_HEADERS, ...options.headers },
  });

  if (!res.ok) {
    let message = `Request failed: ${res.status} ${res.statusText}`;
    try {
      const body: ApiErrorDetail = await res.json();
      if (body?.detail) {
        if (typeof body.detail === "string") message = body.detail;
        else if (Array.isArray(body.detail) && body.detail[0]?.msg) message = body.detail[0].msg;
        else if (Array.isArray(body.detail) && body.detail[0]?.message) message = body.detail[0].message;
      }
    } catch {
      // 非 JSON 时用 statusText
    }
    throw new Error(message);
  }

  const contentType = res.headers.get("content-type");
  if (contentType?.includes("application/json")) return res.json() as Promise<T>;
  return undefined as T;
}

/** GET 请求 */
export async function apiGet<T = unknown>(path: string): Promise<T> {
  return apiRequest<T>(path, { method: "GET" });
}

/** POST 请求 */
export async function apiPost<T = unknown>(path: string, body?: object): Promise<T> {
  return apiRequest<T>(path, {
    method: "POST",
    body: body ? JSON.stringify(body) : undefined,
  });
}
