<template>
    <div class="container-fluid">
        <div class="row">

            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Map at a specified location" headerTitle="true"
                text="true" :desc="desc">
                <GoogleMap api-key="AIzaSyDGCQvcXUsXwCdYArPXo72dLZ31WS3WQRw" :center="{ lat: 20.5937, lng: 78.9629 }"
                    :zoom="12" style="width: auto; height: 500px">
                </GoogleMap>
            </Card3>
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Multi-language support" headerTitle="true"
                text="true" :desc="desc1">
                <GoogleMap api-key="AIzaSyDGCQvcXUsXwCdYArPXo72dLZ31WS3WQRw" :center="{ lat: 20.5937, lng: 78.9629 }"
                    :zoom="6" style="width: auto; height: 500px" :options="{
                        region: 'VI',
                        language: 'vi',
                    }">
                </GoogleMap>
            </Card3>
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Marker on the Map" headerTitle="true" text="true"
                :desc="desc2">
                <Markers></Markers>
            </Card3>
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Draggable Marker" headerTitle="true" text="true"
                :desc="desc3">
                <DraggableMarker></DraggableMarker>
            </Card3>
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Polyline on the Map" headerTitle="true"
                text="true" :desc="desc4">
                <GooglePolyline></GooglePolyline>
            </Card3>
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Polygon on the Map" headerTitle="true" text="true"
                :desc="desc5">
                <TrianglePolygon></TrianglePolygon>
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue';
import { GoogleMap, } from "vue3-google-map";
let Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const Markers = defineAsyncComponent(() => import("@/components/theme/maps/MarkersMap.vue"))
const DraggableMarker = defineAsyncComponent(() => import("@/components/theme/maps/DraggableMarker.vue"))
const GooglePolyline = defineAsyncComponent(() => import("@/components/theme/maps/GooglePolyline.vue"))
const TrianglePolygon = defineAsyncComponent(() => import("@/components/theme/maps/TrianglePolygon.vue"))
let desc = ref<string>("Display a map at a specified location and zoom level.")
let desc1 = ref<string>("Display a map with labels in a foreign language")
let desc2 = ref<string>("Display a map highlighting points of interest")
let desc3 = ref<string>("Display a map highlighting points of interest")
let desc4 = ref<string>("Display a map with a line showing a known route")
let desc5 = ref<string>("Display a map highlighting a region or area")
</script>