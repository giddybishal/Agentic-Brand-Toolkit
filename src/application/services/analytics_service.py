from typing import Dict
from ...domain.models.social_media import SocialMediaProfile
from ...domain.models.analytics import EngagementMetrics

class EngagementAnalyticsService:
    def compute_metrics(self, profile: SocialMediaProfile) -> EngagementMetrics:
        if not profile.posts:
            return EngagementMetrics(
                brand_name=profile.brand_name,
                average_likes=0.0,
                average_comments=0.0,
                average_shares=0.0,
                posting_frequency="Unknown",
                content_type_distribution={}
            )

        total_likes = sum(post.likes for post in profile.posts)
        total_comments = sum(post.comments for post in profile.posts)
        total_shares = sum(post.shares for post in profile.posts)
        num_posts = len(profile.posts)

        type_counts: Dict[str, int] = {}
        for post in profile.posts:
            ctype = post.content_type
            type_counts[ctype] = type_counts.get(ctype, 0) + 1

        distribution = {ctype: (count / num_posts) for ctype, count in type_counts.items()}

        return EngagementMetrics(
            brand_name=profile.brand_name,
            average_likes=round(total_likes / num_posts, 2),
            average_comments=round(total_comments / num_posts, 2),
            average_shares=round(total_shares / num_posts, 2),
            posting_frequency=f"{num_posts} posts analyzed",
            content_type_distribution=distribution
        )
