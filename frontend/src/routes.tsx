import {
  createRouter,
  createRootRoute,
  createRoute,
  Outlet,
  redirect,
} from "@tanstack/react-router";

import Todos from "./pages/Todos";
import App from "./App";

const rootRoute = createRootRoute({
  component: () => (
    <div>
      <Outlet />
    </div>
  ),
});

const homeRoute = createRoute({
  path: "/",
  getParentRoute: () => rootRoute,
  component: App,
});

const todosRoute = createRoute({
  path: "/todos",
  getParentRoute: () => rootRoute,
  component: Todos,
  loader: async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      throw redirect({ to: "/" }); // not logged in
    }
    return null;
  },
});

const routeTree = rootRoute.addChildren([homeRoute, todosRoute]);

export const router = createRouter({ routeTree });
