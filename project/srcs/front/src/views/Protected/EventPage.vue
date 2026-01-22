<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';

    const activeTab = ref('all');
    const events = ref([
        { type: 'sender', from: '@idkart', to: '@gkleier', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'pending' },
        { type: 'receiver', from: '@gkleier', to: '@idkart', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'pending' },
        { type: 'sender', from: '@idkart', to: '@gkleier', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'accepted' },
        { type: 'receiver', from: '@gkleier', to: '@idkart', date: '24 Feb 2026 - 18:00', location: 'Cafe Audelice', message: "Let's meet and talk 😊", status: 'declined' },
    ])

    const filteredEvents = computed(() => {
        if (activeTab.value === 'all')
            return events.value
        if (activeTab.value === 'sent') 
            return events.value.filter(e => e.type === 'sender')
        if (activeTab.value === 'received') 
            return events.value.filter(e => e.type === 'receiver')
        return events.value
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

const EventsData = ref<UserDatesResponse[] | null>(null);
const fetchEvents = async () => {
  isLoading.value = true;
  try {
    const { data } = await EventService.get_my_dates();

    console.log(`data ${data.data}`)
    if (data.data) EventsData.value = [...data.data];
  } catch(err : unknown) {
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

</script>

<template>
    <div class="page">
        <div class="content">
            <nav class="tab">
                <div class="link" :class="{ active: activeTab == 'all' }" @click="setActive('all')">All Events</div>
                <div class="link" :class="{ active: activeTab == 'sent' }" @click="setActive('sent')">Event sent</div>
                <div class="link" :class="{ active: activeTab == 'received' }" @click="setActive('received')">Event received</div>
            </nav>

            <div class="events">
                <div v-for="(event, index) in filteredEvents" :key="index" class="event-card">
                    <div class="users">
                        <span class="user">
                            <img src="/img/profilePictureDemo.png" :alt="event.from" width="45" height="45" />
                            <p>{{ event.from }}</p>
                        </span>
                        <span>
                            <img src="/img/arrow.svg"/>
                        </span>
                        <span class="user">
                            <img src="/img/profilePictureDemo.png" :alt="event.to" width="45" height="45" />
                            <p>{{ event.to }}</p>
                        </span>
                    </div>
                    <div class="details">
                        <div class="date_location">
                            <div class="info">
                                <img src="/img/CalendarEvent.svg" alt="date" />
                                <p>{{ event.date }}</p>
                            </div>
                            <div class="info">
                                <img src="/img/MapEvent.svg" alt="location" />
                                <p>{{ event.location }}</p>
                            </div>
                        </div>
                        <div class="info">
                            <img src="/img/MessageEvent.svg" alt="message" />
                            <p>{{ event.message }}</p>
                        </div>
                    </div>
                    <div class="status" v-if="event.type === 'sender'">
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
                    <div class="confirmation" v-if="event.type === 'receiver'">
                        <button v-if="event.status === 'pending'" class="btn-decline">
                            <img src="/img/DeclineEvent.svg" alt="decline" />
                        </button>
                        <button v-if="event.status === 'pending'" class="btn-accept">
                            <img src="/img/AcceptEventDark.svg" alt="accept" />
                        </button>
                        <div class="status" v-if="event.status === 'declined'">
                            <span class="declined" >
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
.page{
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

.tab{
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
        display: grid;
        align-items: center;
        grid-template-columns: minmax(200px, 250px) 1fr min-content;
        background: $components-background-color;
        padding: 3rem 2rem;
        border-radius: 8px;
        .users {
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
            // flex: 1;
            margin-left: 1rem;
            display: flex;
            gap: 40px;
            // width: 100%;
            .info {
                display: flex;
                align-items: center;
                height: fit-content;
                // width: auto;
                gap: 8px;
            }

            .date_location{
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

            button{
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
    .events {
        .event-card {
            grid-template-columns: 1fr;
            gap: 1.5rem;
            padding: 2rem 2rem;
            font-size: 13px;
            .details {
                flex-direction: column;
                margin-left: 0;
                gap: 10px;
            }
            .status {
                width: fit-content;
                justify-content: flex-end;
            }
            .confirmation {
                justify-content: flex-end;
            }
            .confirmation {
                button{
                    height: 40px;
                    width: 40px;
                }
            }
        }
    }
}

</style>