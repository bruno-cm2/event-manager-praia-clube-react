import Add, * as add from './views/Add'
import Eventos, * as eventos from './views/Eventos'
import Locais, * as locais from './views/Locais'
import Account, * as account from './views/Account'

import './Pages.css'

export const DEFAULT = 'add'

export const VIEWS = {
  add:     { component: Add,     header: add.header,     size: 7},
  eventos: { component: Eventos, header: eventos.header, size: 12},
  locais:  { component: Locais,  header: locais.header,  size: 12},
  account: { component: Account, header: account.header, size: 7}
}