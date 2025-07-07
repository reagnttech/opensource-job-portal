import logging
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse

from mpcomp.views import get_social_referer, get_meta
from peeldb.models import JobPost, State, JOB_TYPE

# Set up logging
logger = logging.getLogger(__name__)


def index(request):
    """
    Homepage view with error handling for robustness.
    """
    try:
        # Try to get cached jobs first
        latest_jobs_list = cache.get("latest_1hr_jobs_list")
        if not latest_jobs_list:
            try:
                latest_jobs_list = (
                    JobPost.objects.filter(status="Live")
                    .exclude(job_type="walk-in")
                    .select_related("company", "user")
                    .prefetch_related("location", "skills")[:9]
                )
                cache.set("latest_1hr_jobs_list", latest_jobs_list, 60 * 60)
            except Exception as job_error:
                logger.error(f"Error fetching jobs: {job_error}")
                latest_jobs_list = []

        # Fallback: Try to get fresh jobs if cached query failed
        if not latest_jobs_list:
            try:
                latest_jobs_list = (
                    JobPost.objects.filter(status="Live")
                    .exclude(job_type="walk-in")
                    .select_related("company", "user")
                    .prefetch_related("location", "skills")[:9]
                )
            except Exception as job_error:
                logger.error(f"Error fetching fresh jobs: {job_error}")
                latest_jobs_list = []

        # Get social referer with fallback
        try:
            field = get_social_referer(request)
            show_pop = True if field == "fb" or field == "tw" or field == "ln" else False
        except Exception as social_error:
            logger.error(f"Error getting social referer: {social_error}")
            field = "otr"
            show_pop = False

        # Get meta data with fallback
        try:
            meta_title, meta_description, h1_tag = get_meta("home_page", {"page": 1})
        except Exception as meta_error:
            logger.error(f"Error getting meta data: {meta_error}")
            meta_title = "PeelJobs - Find Your Dream Job"
            meta_description = "Discover thousands of job opportunities across various industries. Find your perfect career match with PeelJobs."
            h1_tag = "Find Your Dream Job"

        # Get states with fallback
        try:
            states = State.objects.filter(status="Enabled")
        except Exception as state_error:
            logger.error(f"Error fetching states: {state_error}")
            states = []

        # Prepare data with fallbacks
        data = {
            "jobs_list": latest_jobs_list,
            "show_pop_up": show_pop,
            "meta_title": meta_title,
            "meta_description": meta_description,
            "job_types": JOB_TYPE,
            "h1_tag": h1_tag,
            "states": states,
        }

        template = "index.html"
        return render(request, template, data)

    except Exception as e:
        # Final fallback for any unexpected errors
        logger.error(f"Critical error in homepage view: {e}")
        
        # Return minimal working page
        fallback_data = {
            "jobs_list": [],
            "show_pop_up": False,
            "meta_title": "PeelJobs - Job Portal",
            "meta_description": "Job Portal",
            "job_types": [
                ("full-time", "Full Time"),
                ("internship", "Internship"),
                ("walk-in", "Walk-in"),
                ("government", "Government"),
                ("Fresher", "Fresher"),
            ],
            "h1_tag": "Job Portal",
            "states": [],
        }
        
        return render(request, "index.html", fallback_data)
