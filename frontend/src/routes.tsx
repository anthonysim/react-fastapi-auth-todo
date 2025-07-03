import {
  createRouter,
  createRootRoute,
  createRoute,
  Outlet,
  redirect,
} from "@tanstack/react-router";

import Todos from "./pages/Todos";
import App from "./App";

import { auth } from "./auth/auth";

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
    if (!auth.isAuthenticated) {
      throw redirect({ to: "/" });
    }
    return null;
  },
});

const routeTree = rootRoute.addChildren([homeRoute, todosRoute]);

export const router = createRouter({ routeTree });
