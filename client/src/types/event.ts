export interface Event {
  eventId: number
  name: string
  startDate: string
  endDate: string
  description: string
  isPublic: boolean
  isArchived: boolean
  teamId: number | null
  totalMileage: number
}

export interface EventError {
  name?: string[]
  startDate?: string[]
  endDate?: string[]
  description?: string[]
  nonFieldErrors?: string[]
}
