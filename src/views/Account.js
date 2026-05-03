export const header =(
  <>
    <i className="header bi bi-person-circle text-dark"></i><h2>Conta</h2>
  </>
)

export default function Account(){
  return (
    <div className="d-flex flex-column gap-4">

      {/* NOME */}
      <div className="row g-2">
        <div className="col">
          <input type="text" className="form-control" id="nome" placeholder="Nome"/>
        </div>
        <div className="col">
          <input type="text" className="form-control" id="sobrenome" placeholder="Sobrenome"/>
        </div>
      </div>

      {/* SETOR */}
      <input type="text" className="form-control" id="setor" placeholder="Setor" disabled/>

      {/* EMAIL */}
      <div className="input-group">
        <input type="text" className="form-control" id="email" placeholder="Email" disabled/>
        <span className="input-group-text">@praiaclube.org.br</span>
      </div>

      {/* SENHA */}

      <div className="row g-2" id="panel-main">
        <div className="col">
          <input type="password" className="form-control" id="senha" placeholder="Senha" disabled/>
        </div>
        <div className="col-auto">
          <button id="change-btn" className="btn btn-light btn-outline-secondary">Alterar senha</button>
        </div>
      </div>

      <div className="d-flex flex-column gap-4 d-none" id="panel-change">
        <div className="pass-input input-group">
          <input type="password" className="form-control" id="old-pass" placeholder="Senha antiga"/>
          <button className="btn btn-light btn-outline-secondary">
            <i className="bi bi-eye-fill"></i>
          </button>
        </div>
        <div className="pass-input input-group">
          <input type="password" className="form-control" id="new-pass" placeholder="Nova senha"/>
          <button className="btn btn-light btn-outline-secondary">
            <i className="bi bi-eye-fill"></i>
          </button>
        </div>
        <div className="d-flex gap-2 justify-content-end">
          <button id="save-btn" className="btn btn-light btn-outline-secondary">Salvar</button>
          <button id="cancel-btn" className="btn btn-light btn-outline-secondary">Cancelar</button>
        </div>
      </div>
    </div>
  )
  
}