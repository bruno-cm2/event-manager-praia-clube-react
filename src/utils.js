export function clamp(value, min, max) {
  value = Number(value)
  if (Number.isNaN(value)) return ''
  return Math.min(Math.max(value, min), max)
}

export function capital(str) {
  str = String(str)
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export function isInside(x, y, folga = 0) {
  folga *= 60 * 1000
  const depois = y.inicio ? new Date(y.inicio).getTime() < (new Date(x.fim).getTime() - folga + 1000) : true
  const antes = y.fim ? new Date(x.inicio).getTime() < (new Date(y.fim).getTime() + folga - 1000) : true
  return antes && depois
}

export function hora(date) {
  return new Date(date).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

export function data(date) {
  return new Date(date).toLocaleDateString('pt-BR', { month: 'numeric', day: 'numeric' })
}

export function datahora(date, termo = 'às') {
  const d = new Date(date)
  const dt = d.toLocaleDateString('pt-BR', { month: 'numeric', day: 'numeric' })
  const hr = d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  return `${dt} ${termo} ${hr}`
}