import { DayPilot } from '@daypilot/daypilot-lite-vue';
export const data = [
    {
        id: 1,
        start: DayPilot.Date.today().addHours(10),
        end: DayPilot.Date.today().addHours(11),
        text: 'Create Detail Page',
    },
    {
        id: 2,
        start: DayPilot.Date.today().addHours(13),
        end: DayPilot.Date.today().addHours(16),
        text: 'Profile Landing Page',
    },
    {
        id: 3,
        start: "2024-01-22T10:00:00",
        end: "2024-01-22T14:00:00",
        text: "Team Meeting",
        backColor: "#6aa84f",
        borderColor: "#38761d",
    },
    {
        id: 4,
        start: "2024-01-24T02:00:00",
        end: "2024-01-24T03:00:00",
        text: "Event 2",
        backColor: "#f1c232",
        borderColor: "#bf9000",
    },
]