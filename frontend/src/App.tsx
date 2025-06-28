import { useEffect, useState } from "react";
import { AuthAction, AuthPrompt } from "./types/types";

function App() {
  const [msg, setMsg] = useState("");
  const [isSignIn, setIsSignIn] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/hello")
      .then((res) => res.json())
      .then((data) => setMsg(data.message));
  }, []);

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
            className="w-full px-4 py-2 placeholder-gray-400 bg-gray-800 border border-gray-700 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-2 placeholder-gray-400 bg-gray-800 border border-gray-700 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button
            className={`w-full py-2 rounded text-white font-semibold transition ${actionColor}`}
            onClick={() => console.log(`${title} Clicked`)}
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
