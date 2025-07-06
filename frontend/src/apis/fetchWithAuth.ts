export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const accessToken = localStorage.getItem("access_token");

  let res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (res.status === 401) {
    const refreshRes = await fetch(`${import.meta.env.VITE_API_URL}/refresh`, {
      method: "POST",
      credentials: "include", // to send cookies
    });

    if (refreshRes.ok) {
      const data = await refreshRes.json();
      localStorage.setItem("access_token", data.access_token);

      res = await fetch(url, {
        ...options,
        headers: {
          ...(options.headers || {}),
          Authorization: `Bearer ${data.access_token}`,
        },
      });
    } else {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }
  }

  return res;
}
