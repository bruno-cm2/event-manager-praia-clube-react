export const header = (
  <>
    <i className="header bi bi-calendar2-event-fill text-success"></i>
    <h2>Lista de Eventos</h2>
  </>
)

export default function Eventos(){
  return (
    <div className="d-flex flex-column flex-grow-1">
      <div className="row g-2 mb-2">
        <div className="col-6">
          <input id="busca" className="form-control" placeholder="Pesquisar evento"/>
        </div>
        <div className="col-6">
          <div className="dropdown">
            <button id="periodo" className="btn btn-outline-secondary text-start dropdown-toggle w-100" data-bs-toggle="dropdown" data-bs-auto-close="outside" data-bs-display="static">Período</button>
            <div className="dropdown-menu shadow-sm p-0">
              <div id="calendario-periodo"></div>
            </div>
          </div>
        </div>
      </div>

      <div className="d-flex gap-2 flex-grow-1">
        <select id="eventos" className="form-select h-100" multiple></select>
        <select id="config" className="form-select h-100" multiple></select>
      </div>

      <div className="mt-2 d-flex align-items-center">
        <div className="form-check form-switch">
          <input className="form-check-input" type="checkbox" id="criados"/>
          <label className="form-check-label text-nowrap" for="criados">Meus eventos</label>
        </div>
        <div className="d-flex gap-2 ms-auto">
          <button id="add-btn" className="btn btn-primary">Adicionar</button>
          <button id="edit-btn" className="btn btn-secondary">Editar</button>
          <button id="del-btn" className="btn btn-danger">Apagar</button>
        </div>
      </div>
    </div>
  )
}