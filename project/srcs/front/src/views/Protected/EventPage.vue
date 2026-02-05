<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useSocketStore } from '@/stores/socket'

const activeTab = ref('all');
// const events = ref([
//     { type: 'sender', from: '@idkart', to: '@gkleier', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'pending' },
//     { type: 'receiver', from: '@gkleier', to: '@idkart', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'pending' },
//     { type: 'sender', from: '@idkart', to: '@gkleier', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'accepted' },
//     { type: 'receiver', from: '@gkleier', to: '@idkart', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'declined' },
// ])
// const EventsData = ref<UserDatesResponse[] | null>(null);

import useUserStore from '@/stores/user';

const current = useUserStore()
const filteredEvents = computed(() => {
    if (!socketStore.getEventsData) return socketStore.getEventsData
    if (activeTab.value === 'all')
        return socketStore.getEventsData
    if (activeTab.value === 'sent')
        return socketStore.getEventsData.filter(e => e.proposer_id === current.getUserID)
    if (activeTab.value === 'received')
        return socketStore.getEventsData.filter(e => e.proposer_id !== current.getUserID)
    return socketStore.getEventsData
})

function setActive(tab: string) {
    activeTab.value = tab;
}

import axios, { AxiosError } from 'axios';
import type { UserDatesResponse } from '@/types/apiResponses'

import EventService from '@/api/services/EventService';
const isLoading = ref(true);
const isError = ref<string | null>(null);

interface BackendError {
    error: string;
}

const fetchEvents = async () => {
    isLoading.value = true;
    try {
        const { data } = await EventService.get_my_dates();
        if (data.data) socketStore.setEventsData([...data.data])
        // if (data.data) socketStore.getEventsData = [...data.data];
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Registration failed for unknown reason'";
        }
    } finally {
        isLoading.value = false;
    }
};

onMounted(fetchEvents);


const socketStore = useSocketStore()


const actionDate = async (id: number, status: string) => {
    isLoading.value = true;
    try {
        socketStore.respond_to_date(id, status)
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Registration failed for unknown reason'";
        }
    } finally {
        isLoading.value = false;
    }
}

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

import Loading from '@/components/Loading.vue';

</script>

<template>
    <Loading v-if="isLoading" @finished="isLoading = false" />

    <div  v-if="!isLoading && !isError" class="page">
        <div class="content">
            <nav class="tab">
                <div class="link" :class="{ active: activeTab == 'all' }" @click="setActive('all')">All Events</div>
                <div class="link" :class="{ active: activeTab == 'sent' }" @click="setActive('sent')">Event sent</div>
                <div class="link" :class="{ active: activeTab == 'received' }" @click="setActive('received')">Event
                    received</div>
            </nav>

            <div class="events">
                <div v-for="(event, index) in filteredEvents" :key="index" class="event-card">
                    <div class="users">
                        <span class="user">
                            <img :src="pictures_handler(event.proposer_avatar[0].url)" :alt="event.proposer_username" width="45"
                                height="45" />
                            <p>{{ event.proposer_username }}</p>
                        </span>
                        <span>
                            <img src="/img/arrow.svg" />
                        </span>
                        <span class="user">
                            <img :src="pictures_handler(event.partner_avatar[0].url)" :alt="event.partner_username" width="45"
                                height="45" />
                            <p>{{ event.partner_username }}</p>
                        </span>
                    </div>
                    <div class="details">
                        <div class="date_location">
                            <div class="info">
                                <img src="/img/CalendarEvent.svg" alt="date" />
                                <p>{{ event.scheduled_at }}</p>
                            </div>
                            <div class="info">
                                <img src="/img/MapEvent.svg" alt="location" />
                                <p>{{ event.location }}</p>
                            </div>
                        </div>
                        <div class="info" v-if="event.description">
                            <img src="/img/MessageEvent.svg" alt="message" />
                            <p>{{ event.description }}</p>
                        </div>
                    </div>
                    <div class="status" v-if="event.proposer_id === current.getUserID">
                        <span class="pending" v-if="event.status === 'pending'">
                            <img src="/img/PendingEvent.svg" alt="pending" />
                            <p>Pending</p>
                        </span>
                        <span class="accepted" v-else-if="event.status === 'accepted'">
                            <img src="/img/AcceptEventDark.svg" alt="pending" />
                            <p>Accepted</p>
                        </span>
                        <span class="declined" v-else-if="event.status === 'declined'">
                            <img src="/img/DeclineEvent.svg" alt="declined" />
                            <p>Declined</p>
                        </span>
                    </div>
                    <div class="confirmation" v-if="event.proposer_id !== current.getUserID">
                        <button v-if="event.status === 'pending'" class="btn-decline">
                            <img src="/img/DeclineEvent.svg" alt="decline" @click="actionDate(event.id, 'declined')" />
                        </button>
                        <button v-if="event.status === 'pending'" class="btn-accept">
                            <img src="/img/AcceptEventDark.svg" alt="accept" @click="actionDate(event.id,'accepted')" />
                        </button>
                        <div class="status" v-if="event.status === 'declined'">
                            <span class="declined">
                                <img src="/img/DeclineEvent.svg" alt="declined" />
                                <p>Declined</p>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.page {
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 0.5%;
}

.content {
    display: flex;
    flex-direction: column;
}

nav {
    display: flex;
    gap: 25px;
    margin-bottom: 30px;
}

.tab {
    width: 100%;
}

.link {
    cursor: pointer;
    text-decoration: none;
    color: $text-color;
    padding-bottom: 5px;
    font-weight: 600;

    &:hover {
        border-style: solid;
        border-width: 0px 0px 5px 0px;
        border-color: $border-color-hover;
    }

    &.active {
        border-style: solid;
        border-width: 0px 0px 5px 0px;
        border-color: $border-color-active;
    }
}

.events {
    display: flex;
    flex-direction: column;
    gap: 1rem;

    .event-card {
        // display: grid;
        // grid-template-columns: minmax(200px, 250px) auto;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        background: $components-background-color;
        padding: 3rem 2rem;
        border-radius: 8px;
        gap: 30px;
        // height: auto;
        .users {
            // flex: 1;
            display: flex;
            gap: 0.5rem;
            align-items: center;
            .user {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.25rem;

                img {
                    border-radius: 50%;
                }
            }
        }

        .details {
            // margin-left: 1rem;
            flex: 1 1 auto;
            display: flex;
            flex-wrap: wrap;
            gap: 40px;
            .info {
                display: flex;
                align-items: center;
                height: fit-content;
                gap: 8px;
            }

            .date_location {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
        }

        .status {
            span {
                white-space: nowrap;
                padding: 10px 15px;
                border-radius: 20px;
                background: $components-background-color;
                display: flex;
                align-items: center;
                gap: 5px;
                font-weight: 600;
            }

            .accepted {
                background: #e2bdf697;
                color: #382343;
            }

            .pending {
                color: #E2BDF6;
            }

            .declined {
                color: #E2BDF6;
            }
        }

        .confirmation {
            display: flex;

            button {
                background: none;
                border: none;
                cursor: pointer;
                margin-left: 10px;
                border-radius: 10px;
                height: 50px;
                width: 50px;
                transition: 0.3s;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .btn-accept {
                background-color: #E2BDF6;
            }

            .btn-decline {
                background: $components-background-color;
            }

            button:hover {
                filter: brightness(0.9);
                transition: 0.3s;
            }
        }
    }

}

@media (max-width: $breakpoint-md) {
    // .events {
    //     .event-card {
    //         grid-template-columns: 1fr;
    //         gap: 1.5rem;
    //         padding: 2rem 2rem;
    //         font-size: 13px;

    //         .details {
    //             flex-direction: column;
    //             margin-left: 0;
    //             gap: 10px;
    //         }

    //         .status {
    //             width: fit-content;
    //             justify-content: flex-end;
    //         }

    //         .confirmation {
    //             justify-content: flex-end;
    //         }

    //         .confirmation {
    //             button {
    //                 height: 40px;
    //                 width: 40px;
    //             }
    //         }
    //     }
    // }
}
</style>