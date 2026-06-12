BRAND_PROFILE_PROMPT = """
You are an expert brand strategist. Your task is to extract a comprehensive brand profile from the provided website content.
Focus on identifying the core identity, what they do, who they serve, and what they stand for.

Input Website Content:
{content}

Extract and generate the following fields:
1. brand_name: The name of the brand.
2. industry: The primary industry or market category.
3. mission: The brand's mission statement or core purpose.
4. description: A clear, concise description of the company.
5. products: A list of key products, services, or features offered.
"""

CREATOR_GUIDELINES_PROMPT = """
You are an expert brand manager and influencer marketer. Your task is to generate practical, creator-focused guidelines based on the provided Brand Profile.
These guidelines will be used by content creators (influencers, UGC creators) to produce authentic content that aligns with the brand's identity.

Brand Profile:
{brand_profile}

Generate the following fields:
1. tone_of_voice: Describe the brand's tone of voice (e.g., "Playful and energetic", "Professional and trustworthy").
2. dos: A list of practical "Do's" for creators (e.g., "Do show the product in natural lighting", "Do use casual, everyday language").
3. donts: A list of practical "Don'ts" for creators (e.g., "Don't mention competitors", "Don't use overly scripted or formal language").
4. content_suggestions: A list of creative content ideas or hooks that would work well for this brand.

Ensure the guidelines are actionable, specific, and avoid generic marketing fluff.
"""
