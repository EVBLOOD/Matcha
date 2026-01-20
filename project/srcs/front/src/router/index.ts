import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import EmailConfirmationPage from '@/views/EmailConfirmationPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ResetPage from '@/views/ResetPage.vue';
import UpdatePassword from '@/views/UpdatePassword.vue';
import ProfileOnboarding from '@/views/ProfileOnboarding.vue';
import HomePage from '@/views/Protected/HomePage.vue';
import ExplorePage from '@/views/Protected/ExplorePage.vue';
import SuggestionsPage from '@/views/Protected/SuggestionsPage.vue';
import MessagesPage from '@/views/Protected/MessagesPage.vue';
import NotificationsPage from '@/views/Protected/NotificationsPage.vue';
import ProfilePage from '@/views/Protected/ProfilePage.vue';
import Vue from '@/views/Protected/profile/View.vue';
import ViewSettings from '@/views/Protected/profile/ViewSettings.vue';
import ViewSettingsMore from '@/views/Protected/profile/ViewSettingsMore.vue';
import ViewSettingsDefault from '@/views/Protected/profile/ViewSettingsDefault.vue';
import ViewBlocks from '@/views/Protected/profile/ViewBlocks.vue';
import ViewSeens from '@/views/Protected/profile/ViewSeens.vue';
import VueInteractions from '@/views/Protected/profile/VueInteractions.vue';
import ViewLikes from '@/views/Protected/profile/ViewLikes.vue';
import ViewSettingsPassword from '@/views/Protected/profile/ViewSettingsPassword.vue';




// import Conversation from '@/views/Protected//chat/Conversation.vue';
import Conversation from '@/views/Protected/chat/Calls.vue';

import OauthPage from '@/views/OauthPage.vue';


import useUserStore from '@/stores/user';
import { useSocketStore } from '@/stores/socket';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomePage,
      meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true },
      children: [
        {
          path: '',
          name: 'home',
          component: ExplorePage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Explore' },
        },
        {
          path: 'suggestions',
          name: 'suggestions',
          component: SuggestionsPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Suggestions' },
        },
        {
          path: 'messages',
          component: MessagesPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Chat' },
          children: [
            {
                path: ':id',
                component: Conversation,
                meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Chat' }
            },
          ]
        },
        {
          path: 'notifications',
          component: NotificationsPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Notifications' }
        },
        {
          path: 'profile/:id',
          component: ProfilePage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile' },
          children: [
            {
              path: '',
              component: Vue,
              meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile' },
            },
            {
              path: 'settings',
              component: ViewSettings,
              meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Personal details' },
              children : [
                {
                  path: '',
                  component: ViewSettingsDefault,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Personal details' }
                },
                {
                  path: 'password',
                  component: ViewSettingsPassword,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Change password' }
                },
                {
                  path: 'details',
                  component: ViewSettingsMore,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'More details' }
                }
              ]
            },
            {
              path: 'interactions',
              component: VueInteractions,
              meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'Personal Interactions' },
              children : [
                {
                  path: '',
                  component: ViewLikes,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'View Likes List' }
                },
                {
                  path: 'vues',
                  component: ViewSeens,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'View Visitors' }
                },
                {
                  path: 'blocks',
                  component: ViewBlocks,
                  meta: { requiresSameUser: true, requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile', subtitle: 'View Block List' }
                }
              ]
            }
          ]
        },
      ]
    },
    {
      path: '/landing',
      name: 'landing',
      component: LandingPage,
      meta: { public: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: { public: true }
    },
    {
      path: '/confirm-email', // TODO: I should find a solution to integrate this later
      name: 'email confirmation',
      component: EmailConfirmationPage,
      meta: { requiresVerification: false, requiresAuth: true, requiresCompleteProfile: false }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { public: true }
    },
    {
      path: '/reset-password',
      name: 'reset',
      component: ResetPage,
      meta: { public: true }
    },
    {
      path: '/new-password',
      name: 'new-password',
      component: UpdatePassword,
      meta: { public: true }
    },
    {
      path: '/auth-success',
      name: 'oauth',
      component: OauthPage,
      meta: { public: true }
    },
    {
      path: '/profile-onboarding',
      name: 'profile onboarding',
      component: ProfileOnboarding,
      meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: false }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const user = useUserStore();
  const socketStore = useSocketStore();
  const token = localStorage.getItem('auth_token');

  if (token && !user.isLoaded) {
    try {
      await user.fetchUser();
    } catch (err) {
      localStorage.removeItem('auth_token');
      user.resetStore();
    }
  }

  if (!token && user.isAuthenticated) {
    user.resetStore(); 
  }

  if (!user.isAuthenticated) {
    if (to.meta.public) {
      return next();
    }
    return next({ name: 'login' });
  }

  if (to.meta.public) {
    return next({ name: 'home' });
  }

  if (!user.isVerified && to.meta.requiresVerification && to.name !== 'email confirmation') {
    return next({ name: 'email confirmation' });
  }

  if (user.isVerified && !user.isProfileComplete && to.meta.requiresCompleteProfile && to.name !== 'profile onboarding') {
    return next({ name: 'profile onboarding' });
  }

  if (to.meta.requiresSameUser && to.params.id != user.getUserID) {
    return next({ name: 'home' });
  }

  if (user.isVerified && user.isProfileComplete) {
    socketStore.connectAll();
  }

  next();
});
export default router
