import { useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { AuthAction, AuthPrompt } from "./types/types";

import { fakeRegister } from "./apis/fakeApiCall";

function App() {
  const [msg, setMsg] = useState("");
  const [isSignIn, setIsSignIn] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/hello`)
      .then((res) => res.json())
      .then((data) => setMsg(data.message));
  }, []);

  const handleAuth = async () => {
    const data = fakeRegister(email, password);
    data
      .then(console.log)
      .then(() => alert("Account successfully created. Please login!"));
    // const endpoint = `${import.meta.env.VITE_API_URL}/${isSignIn ? "login" : "register"}`;

    // const body = isSignIn
    //   ? new URLSearchParams({ username: email, password: password })
    //   : JSON.stringify({ email, password });

    // try {
    //   const res = await fetch(endpoint, {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": isSignIn
    //         ? "application/x-www-form-urlencoded"
    //         : "application/json",
    //     },
    //     body,
    //   });

    //   if (!res.ok) throw new Error("Auth failed");

    //   const data = await res.json();
    //   localStorage.setItem("token", data.access_token);
    //   localStorage.setItem("user", JSON.stringify(data.user));

    //   navigate({ to: "/todo" }); // ✅ Redirect
    // } catch (err) {
    //   alert("Failed to authenticate");
    //   console.error(err);
    // }
  };

  const title = isSignIn ? AuthAction.SignIn : AuthAction.Register;
  const actionColor = isSignIn
    ? "bg-blue-600 hover:bg-blue-700"
    : "bg-orange-500 hover:bg-orange-600";
  const toggleText = isSignIn
    ? AuthPrompt.NoAccount
    : AuthPrompt.AlreadyHaveAccount;

  return (
    <div className="flex items-center justify-center min-h-screen p-6 text-white bg-gray-950 sm:p-12">
      <div className="w-full max-w-md p-8 space-y-6 bg-gray-900 border border-gray-800 shadow-lg rounded-2xl">
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-semibold">
            Stateful Auth - React and FastAPI
          </h1>
          <p className="text-sm text-gray-400">
            {msg || "Connecting to backend..."}
          </p>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-medium text-center">{title}</h2>

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 placeholder-gray-400 bg-gray-800 border border-gray-700 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 placeholder-gray-400 bg-gray-800 border border-gray-700 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button
            className={`w-full py-2 rounded text-white font-semibold transition ${actionColor}`}
            onClick={handleAuth}
          >
            {title}
          </button>
        </div>

        <div className="pt-2 text-center">
          <button
            className="text-sm text-blue-400 hover:underline"
            onClick={() => setIsSignIn((prev) => !prev)}
          >
            {toggleText}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
