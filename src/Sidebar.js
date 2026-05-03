import logo from "./logos/logo-praia-light.png";
import "./Sidebar.css";

const LINKS = [
  { href: "add", icon: "bi-pencil-square text-primary", label: "Criar" },
  { href: "eventos", icon: "bi-calendar-event text-success", label: "Eventos" },
  { href: "locais", icon: "bi-geo-alt text-danger", label: "Locais" },
];

export default function Sidebar({ page, setPage }) {
  return (
    <aside className="col-2 shadow p-0">
      <ul className="nav nav-pills d-flex flex-column h-100">
        <img
          src={logo}
          className="img-fluid w-50 mx-auto mt-4 mb-4"
          alt="logo"
        />

        {LINKS.map(({ href, icon, label }) => (
          <li key={href} className="nav-item">
            <a
              className={`nav-link w-100 text-start text-dark ps-4 rounded-0 ${page === href ? "active" : ""}`}
              onClick={() => setPage(href)}
              href={href}
            >
              <i className={`pills bi ${icon}`}></i> {label}
            </a>
          </li>
        ))}

        <li className="nav-item mt-auto mb-3">
          <a
            className={`nav-link w-100 text-start text-dark ps-4 rounded-0 ${page === "account" ? "active" : ""}`}
            onClick={() => setPage("account")}
            href="account"
          >
            <i className="pills bi bi-person-circle text-dark"></i> Conta
          </a>
        </li>
      </ul>
    </aside>
  );
}
