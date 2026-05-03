import { useState } from "react";
import logo from "./logos/logo-praia-light.png";
import "./App.css";
import Sidebar from "./Sidebar";
import { VIEWS, DEFAULT } from "./Pages";
import { capital } from "./utils";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const page = location.pathname.slice(1) || "add";
  const { component: View, header, size } = VIEWS[page] ?? {};
  return (
    <div className="container-fluid p-0" style={{ height: "100dvh" }}>
      <div className="row h-100 g-0">
        <Sidebar page={page} setPage={(p) => navigate(`/${p}`)} />
        <div className="col d-flex p-3">
          <main className="d-flex flex-column flex-grow-1 border rounded-3 shadow-sm bg-white p-4">
            <div
              className="d-flex align-items-center border-bottom pb-1 mb-4"
              id="page-header"
            >
              {header}
            </div>
            <div
              id="content"
              className={`col-${size} d-flex flex-column flex-grow-1`}
            >
              <Routes>
                {Object.entries(VIEWS).map(([path, { component: View }]) => (
                  <Route key={path} path={`/${path}`} element={<View />} />
                ))}
                <Route path="*" element={<VIEWS.add.component />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
