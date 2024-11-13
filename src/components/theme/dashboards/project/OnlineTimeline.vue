<template>
    <div class="col-xl-4 col-xl-100 col-md-6 proorder-md-12">
        <div class="card">
            <div class="card-header card-no-border pb-0">
                <div class="header-top">
                    <h4>Online Course Timeline</h4>
                    <div class="dropdown icon-dropdown">
                        <button class="btn dropdown-toggle" id="userdropdown29" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false"><i class="icon-more-alt"></i></button>
                        <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown29"><a
                                class="dropdown-item" href="#">Weekly</a><a class="dropdown-item" href="#">Monthly</a><a
                                class="dropdown-item" href="#">Yearly</a></div>
                    </div>
                </div>
            </div>
            <div class="card-body overflow-auto theme-scrollbar">
                <div class="timeline-calendar custom-scrollbar">
                    <div class="custom-calendar" id="calendar-container">
                        <DayPilotCalendar id="dp" :config="config" ref="calendarRef" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, onMounted, } from 'vue';
import { data } from "@/core/data/timeline"
import { DayPilot, DayPilotCalendar } from '@daypilot/daypilot-lite-vue';
const calendarRef = ref(null);
const config = {
    viewType: "Week",
    startDate: DayPilot.Date.today(),
    onTimeRangeSelected: (args) => {
        DayPilot.Modal.prompt('Create a new event:', 'Event 1').then((modal) => {
            var dp = args.control;
            dp.clearSelection();
            if (modal.canceled) {
                return;
            }
            dp.events.add({
                start: args.start,
                end: args.end,
                id: DayPilot.guid(),
                text: modal.result,
            });
        });
    },
    eventDeleteHandling: 'Disabled',
    onEventMoved: () => {

    },
    onEventResized: () => {

    },
};
const loadEvents = () => {
    calendarRef.value.control.update({ events: data });


};

onMounted(() => {
    loadEvents();
});

</script>
  