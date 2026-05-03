export const header = (
  <>
    <i className="header bi bi-pencil-fill text-primary"></i>
    <h2>Criar Evento</h2>
  </>
)

export default function Add(){
  return (
    <div className="d-flex flex-column gap-4">
    
      <input id="titulo" className="form-control" placeholder="Título"/>

      <div className="col">
        <div className="row g-2">

          <div className="col-4">
            <div className="dropdown w-100">
              <button id="tipo-btn" className="btn btn-outline-secondary w-100 text-start dropdown-toggle" data-bs-toggle="dropdown">
                Tipo
              </button>
              <ul id="tipo" className="dropdown-menu py-1"></ul>
            </div>
          </div>

          <div className="col">
            <div className="input-group dropdown">
              <button id="inicio" className="btn btn-outline-secondary dropdown-toggle flex-grow-1 text-start border-end-0" style={{width: 0}} data-bs-toggle="dropdown" data-bs-auto-close="outside" data-bs-offset="-75%,0">Início</button >
              <div className="dropdown-menu shadow-sm p-0">
                <div id="calendario-inicio"></div>
              </div>
              <button id="rev-btn" className="btn btn-light btn-outline-secondary">
                <i className="bi bi-arrow-left-right flex-grow-0"></i>
              </button>
              <button id="fim" className="btn btn-outline-secondary dropdown-toggle flex-grow-1 text-start  border-start-0 border-end-0" style={{width: 0}} data-bs-toggle="dropdown" data-bs-auto-close="outside" data-bs-offset="-75%,0">Fim</button>
              <div className="dropdown-menu shadow-sm p-0">
                <div id="calendario-fim"></div>
              </div>
              <button id="add-btn" className="btn btn-light btn-outline-secondary">
                <i className="bi bi-plus-lg flex-grow-0"></i>
              </button>
            </div>
          </div>
        </div>

        <div id="datasSelecionadas" className="d-flex flex-wrap gap-2"></div>

      </div>

      <div className="d-flex">  
        <div className="col">

          <div className="dropdown w-100">
            <button className="btn btn-outline-secondary w-100 text-start dropdown-toggle" data-bs-toggle="dropdown" data-bs-auto-close="outside">
              Selecionar locais
            </button>
            <div className="dropdown-menu px-2 shadow-sm w-100">

              <input id="busca-locais" className="form-control mb-2" placeholder="Buscar setor ou quadra"/>

              <div id="lista-locais" style={{overflow:'auto', maxHeight: 220}}></div>
            </div>
          </div>

          <div id="locaisSelecionados" className="d-flex flex-wrap gap-1"></div>

        </div>
      </div>

      <div className="d-flex">
        <div className="col">
          <textarea id="obs" className="form-control" placeholder="Descrição" rows="4"></textarea>
        </div>
      </div>

      <div id="submit" className="d-flex justify-content-end">
        <button id="submit-btn" className="btn btn-outline-secondary rounded" type="submit">Adicionar</button>
      </div>
    </div>
  )
}