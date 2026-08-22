export type Status = 'green' | 'amber' | 'red'

export type Site = {
  id: string
  name: string
  lat: number
  lon: number
  thickness: number
  mass: number | boolean
  pour_cost: number
  re_pour_co2: number
}

export type Cell = {
  id: string
  bounds: number[][]
  tempF: number
  source: string
}

export type ForecastHour = {
  timestamp: string
  hour: string
  tempF: number
  status?: Status
  marginF?: number
  source: string
  rules?: string[]
}

export type DayWindow = {
  date: string
  weekday: string
  range: string
  p25F: number
  p75F: number
  confidence: string
  worst: Status
  source: string
}

export type ModelWindow = {
  hours: ForecastHour[]
  worst: Status
  limitF: number
  amberBandF: number
  source: string
}

export type ApiError = { message: string; source?: string }

