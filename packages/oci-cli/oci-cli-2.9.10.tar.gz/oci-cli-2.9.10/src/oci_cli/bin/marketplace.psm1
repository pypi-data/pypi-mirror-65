function GetOciTopLevelCommand_marketplace() {
    return 'marketplace'
}

function GetOciSubcommands_marketplace() {
    $ociSubcommands = @{
        'marketplace' = 'accepted-agreement agreement category listing package publisher'
        'marketplace accepted-agreement' = 'create delete get list update'
        'marketplace agreement' = 'get list'
        'marketplace category' = 'list'
        'marketplace listing' = 'get list'
        'marketplace package' = 'get list'
        'marketplace publisher' = 'list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_marketplace() {
    $ociCommandsToLongParams = @{
        'marketplace accepted-agreement create' = 'agreement-id compartment-id defined-tags display-name freeform-tags from-json help listing-id package-version signature'
        'marketplace accepted-agreement delete' = 'accepted-agreement-id force from-json help if-match signature'
        'marketplace accepted-agreement get' = 'accepted-agreement-id from-json help'
        'marketplace accepted-agreement list' = 'accepted-agreement-id all compartment-id display-name from-json help limit listing-id package-version page page-size sort-by sort-order'
        'marketplace accepted-agreement update' = 'accepted-agreement-id defined-tags display-name force freeform-tags from-json help if-match'
        'marketplace agreement get' = 'agreement-id from-json help listing-id package-version'
        'marketplace agreement list' = 'all from-json help limit listing-id package-version page page-size'
        'marketplace category list' = 'all from-json help limit page page-size'
        'marketplace listing get' = 'from-json help listing-id'
        'marketplace listing list' = 'all category from-json help is-featured limit listing-id name package-type page page-size pricing publisher-id sort-by sort-order'
        'marketplace package get' = 'from-json help listing-id package-version'
        'marketplace package list' = 'all from-json help limit listing-id package-type package-version page page-size sort-by sort-order'
        'marketplace publisher list' = 'all from-json help limit page page-size publisher-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_marketplace() {
    $ociCommandsToShortParams = @{
        'marketplace accepted-agreement create' = '? c h'
        'marketplace accepted-agreement delete' = '? h'
        'marketplace accepted-agreement get' = '? h'
        'marketplace accepted-agreement list' = '? c h'
        'marketplace accepted-agreement update' = '? h'
        'marketplace agreement get' = '? h'
        'marketplace agreement list' = '? h'
        'marketplace category list' = '? h'
        'marketplace listing get' = '? h'
        'marketplace listing list' = '? h'
        'marketplace package get' = '? h'
        'marketplace package list' = '? h'
        'marketplace publisher list' = '? h'
    }
    return $ociCommandsToShortParams
}