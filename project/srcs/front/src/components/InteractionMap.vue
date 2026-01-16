<script setup lang="ts">
import { LMap, LTileLayer, LMarker, LPopup, LIcon } from "@vue-leaflet/vue-leaflet";
import UserService from '@/api/services/UserService';
import { ref, onMounted } from "vue";
import axios, { AxiosError } from 'axios';
import type { Map as LeafletMap } from "leaflet";
import type { UserLocation, Location } from "@/types/apiResponses";


interface BackendError {
    error: string;
}

const mapRef = ref<LeafletMap | null>(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);
const zoom = ref(13);
const users = ref<UserLocation[]>([]);
const my_location = ref<Location | null>(null);

const center = ref<[number, number]>([33.5731, -7.5898]);

const fetchMyLoc = async () => {
    isLoading.value = true;
    try {
        const { data } = await UserService.get_location_lt_lng();
        my_location.value = data['data'];
        if (my_location.value)
            center.value = [my_location.value.latitude, my_location.value.longitude]
        if (mapRef.value)
            mapRef.value.flyTo(center.value, 14, {
        animate: true,
        duration: 1.5
    });
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Registration failed for unknown reason";
        }
    } finally {
        isLoading.value = false;
    }
};


const fetchRangeLocation = async (query: string) => {
    isLoading.value = true;
    try {
        const { data } = await UserService.get_range_user_locations(query);
        console.log(data)
        users.value = data['data'];
        console.log(data)
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Failed to fetch users";
        }
    } finally {
        isLoading.value = false;
    }
};


const onMapReady = (lmap: LeafletMap) => {
    mapRef.value = lmap;
    fetchMyLoc();

    const bounds = lmap.getBounds();
    const bbox = {
        min_lat: bounds.getSouthWest().lat,
        max_lat: bounds.getNorthEast().lat,
        min_lng: bounds.getSouthWest().lng,
        max_lng: bounds.getNorthEast().lng
    };
    const query = new URLSearchParams(bbox as any).toString();
    fetchRangeLocation(`?${query}`)

};

const onMapMove = (event: any) => {
    const map = event.target;
    const bounds = map.getBounds();

    const bbox = {
        min_lat: bounds.getSouthWest().lat,
        max_lat: bounds.getNorthEast().lat,
        min_lng: bounds.getSouthWest().lng,
        max_lng: bounds.getNorthEast().lng
    };
    const query = new URLSearchParams(bbox as any).toString();
    fetchRangeLocation(`?${query}`)
};


const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}
import type { PointExpression } from 'leaflet';
const iconSize = ref<PointExpression>([32, 32]);
</script>

<template>
    <div class="map-container">
        <l-map 
            ref="mapRef" 
            v-model:zoom="zoom" 
            :center="center" 
            :use-global-leaflet="false"
            @moveend="onMapMove"
            @ready="onMapReady"
        >
            <l-tile-layer 
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" 
                layer-type="base"
                name="OpenStreetMap"
            ></l-tile-layer>

            <l-marker v-for="user in users" :key="user.id" :lat-lng="[user.latitude, user.longitude]">
                <l-icon :icon-url="pictures_handler(user.profile_picture_url[0].url)" :icon-size="iconSize" />
                <l-popup>
                    <strong>{{ user.username }}</strong> <br />
                    <router-link :to="`/profile/${user.id}`">View Profile</router-link>
                </l-popup>
            </l-marker>
        </l-map>
    </div>
</template>

<style scoped>

.map-container {
  height: 500px;
  width: 100%;
  position: relative;
  overflow: hidden !important; 
}

.map-container * {
  overflow: visible !important;
}

.icon-avatar {
    border-radius: 50%;
}

</style>