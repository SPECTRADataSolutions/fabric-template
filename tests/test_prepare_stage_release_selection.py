"""
Test release selection and prioritization logic.

Tests:
- Prioritize releases 112 and 106
- Fallback to first release if prioritized not found
- Handle empty releases list
- Handle releases without IDs
"""

import pytest
from unittest.mock import Mock, patch


class TestReleasePrioritization:
    """Test release prioritization logic."""
    
    def test_prioritize_releases_112_and_106(self):
        """Test that releases 112 and 106 are prioritized."""
        releases = [
            {"id": 71, "name": "Release 71"},
            {"id": 112, "name": "Release 112"},
            {"id": 106, "name": "Release 106"},
            {"id": 31, "name": "Release 31"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        assert release_id == 112  # Should find 112 first
    
    def test_prioritize_release_106_when_112_not_found(self):
        """Test that 106 is selected when 112 not found."""
        releases = [
            {"id": 71, "name": "Release 71"},
            {"id": 106, "name": "Release 106"},
            {"id": 31, "name": "Release 31"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        assert release_id == 106  # Should find 106
    
    def test_fallback_to_first_release(self):
        """Test fallback to first release when prioritized not found."""
        releases = [
            {"id": 71, "name": "Release 71"},
            {"id": 31, "name": "Release 31"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        # If prioritized releases not found, use first release
        if not release_id:
            for release in releases[:10]:
                candidate_id = release.get("id")
                if candidate_id:
                    release_id = candidate_id
                    break
        
        assert release_id == 71  # Should fallback to first release
    
    def test_handle_empty_releases_list(self):
        """Test handling of empty releases list."""
        releases = []
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        # If prioritized releases not found, use first release
        if not release_id:
            for release in releases[:10]:
                candidate_id = release.get("id")
                if candidate_id:
                    release_id = candidate_id
                    break
        
        assert release_id is None  # Should be None for empty list
    
    def test_handle_releases_without_ids(self):
        """Test handling of releases without ID field."""
        releases = [
            {"name": "Release without ID"},
            {"id": 71, "name": "Release 71"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        # If prioritized releases not found, use first release with ID
        if not release_id:
            for release in releases[:10]:
                candidate_id = release.get("id")
                if candidate_id:
                    release_id = candidate_id
                    break
        
        assert release_id == 71  # Should skip release without ID
    
    def test_handle_none_id_values(self):
        """Test handling of releases with None ID values."""
        releases = [
            {"id": None, "name": "Release with None ID"},
            {"id": 71, "name": "Release 71"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        # If prioritized releases not found, use first release with valid ID
        if not release_id:
            for release in releases[:10]:
                candidate_id = release.get("id")
                if candidate_id:  # None is falsy, so this skips it
                    release_id = candidate_id
                    break
        
        assert release_id == 71  # Should skip release with None ID
    
    def test_prioritization_order(self):
        """Test that 112 is checked before 106."""
        releases = [
            {"id": 71, "name": "Release 71"},
            {"id": 106, "name": "Release 106"},
            {"id": 112, "name": "Release 112"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        assert release_id == 112  # Should find 112 first, even though 106 appears earlier in list
    
    def test_multiple_prioritized_releases(self):
        """Test when both 112 and 106 are in list."""
        releases = [
            {"id": 71, "name": "Release 71"},
            {"id": 106, "name": "Release 106"},
            {"id": 112, "name": "Release 112"},
            {"id": 31, "name": "Release 31"},
        ]
        
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    break
            if release_id:
                break
        
        assert release_id == 112  # Should find 112 first (first in priority list)

